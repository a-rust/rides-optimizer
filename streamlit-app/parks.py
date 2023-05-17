import streamlit as st
import pandas as pd
import random
import sys
import os
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
import park_data


class OptimizePark():
    def __init__(self, name: str, all_rides: dict, active_rides: dict, time_assumption: str) -> None:
        self.name = name
        self.all_rides = all_rides
        self.active_rides = active_rides
        self.time_assumption = time_assumption

    def main(self):
        optimization_problem = st.selectbox("Please choose which optimization problem you'd like to solve", ("Maximize Rides", "Minimize Time"), help="Do you want to maximize the total number of rides to go on, or minimize the total amount of time spent at the park?")
        if optimization_problem not in st.session_state:
            st.session_state.optimization_problem = optimization_problem
        time_periods = self.granularity()
        rides = self.park_rides(time_periods)
        required_constraints = self.required_constraints(rides)

    def granularity(self):
        st.sidebar.markdown("<h2 style='text-align: center;'>Time Updates</h2", unsafe_allow_html=True, help="Control the time changes")
        rand_frequency = random.randint(60, 100)
        frequency = st.sidebar.slider("Time Change Frequency (minutes)", min_value=20, max_value=100,  value=rand_frequency, key="frequency_slider", help="How often will the wait/rides times change?")
        rand_time_periods = random.randint(2, 5)
        if "rand_time_periods" not in st.session_state:
            st.session_state.rand_time_periods = rand_time_periods
        time_periods = st.sidebar.slider("How many time periods will there be?", min_value=2, max_value=20, value=st.session_state.rand_time_periods)
        return [time_periods, frequency]

    def park_rides(self, granularity):
        if self.time_assumption == "Constant":
            park_rides = pd.DataFrame({"Rides": list(self.active_rides.keys()), "Wait Times": list(self.active_rides.values())})

        elif self.time_assumption == "Dynamic":
            park_rides = pd.DataFrame({"Rides": list(self.active_rides.keys()), "Wait Times Period 1": list(self.active_rides.values())})
            for i in range(1, granularity[0]):
                park_rides[f'Wait Times Period {i+1}'] = None
        
        st.markdown("<h2 style='text-align: center;'>Active Rides</h2",
                            unsafe_allow_html=True, help="Feel free to add, delete, or edit the rides data")
        experimental_rides_df = st.experimental_data_editor(park_rides, num_rows="fixed")

        return experimental_rides_df

    def required_constraints(self, rides):
        st.sidebar.markdown("<h2 style='text-align: center;'>Required Constraint</h2", unsafe_allow_html=True, help="This constraint must be set to have any meaningful results")
        if st.session_state.optimization_problem == "Maximize Rides":
            rand_max_time_slider = random.randint(len(rides.Rides), 5*len(rides.Rides))
            max_time_slider = st.sidebar.slider("Maximum Time Constraint", max_value=300, value=rand_max_time_slider, help="What is the maximum total amount of time you'd like to spend waiting and riding rides?")
            min_total_rides_slider = None
        elif st.session_state.optimization_problem == "Minimize Time":
            rand_min_total_rides_slider = random.randint(0, len(rides.Rides))
            min_total_rides_slider = st.sidebar.slider("Minimum Number of Total Rides Constraint", max_value=5*len(rides.Rides), value=rand_min_total_rides_slider, help="What is the minimum total number of rides you'd like to go on?")
            max_time_slider = None
        return [max_time_slider, min_total_rides_slider]
