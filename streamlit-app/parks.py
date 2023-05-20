import streamlit as st
import pandas as pd
import random
import sys
import os
import typing

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
import park_data
from optimization import user_preferences as up
from optimization import constant_times as ct
from optimization import dynamic_times as dt
import helper


class OptimizePark():
    def __init__(self, name: str, active_rides: dict, time_assumption: str) -> None:
        self.name = name
        self.active_rides = active_rides
        self.time_assumption = time_assumption

    def main(self):
        global time_periods
        optimization_problem = st.selectbox("Please choose which optimization problem you'd like to solve", ("Maximize Rides", "Minimize Time"), help="Do you want to maximize the total number of rides to go on, or minimize the total amount of time spent waiting in line?")
        if optimization_problem not in st.session_state:
            st.session_state.optimization_problem = optimization_problem
        col1, col2 = st.columns((1, 1))
        if self.time_assumption == "Constant":
            rides = self.park_rides(col1, None)
        elif self.time_assumption == "Dynamic":
            time_periods = self.granularity()
            rides = self.park_rides(col1, time_periods)
        required_constraints = self.required_constraints(rides)
        optional_constraints = self.optional_constraints(rides, required_constraints)
        if self.time_assumption == "Constant":
            self.optimize(col2, rides, optional_constraints, None)
        elif self.time_assumption == "Dynamic":
            self.optimize(col2, rides, optional_constraints, time_periods)

    def granularity(self):
        st.sidebar.markdown("<h2 style='text-align: center;'>Time Updates</h2", unsafe_allow_html=True, help="Control the time changes")
        rand_frequency = random.randint(60, 100)
        frequency = st.sidebar.slider("Time Change Frequency (minutes)", min_value=20, max_value=100,  value=rand_frequency, key="frequency_slider", help="How often will the wait/rides times change?")
        rand_time_periods = random.randint(2, 5)
        if "rand_time_periods" not in st.session_state:
            st.session_state.rand_time_periods = rand_time_periods
        time_periods = st.sidebar.slider("How many time periods will there be?", min_value=2, max_value=20, value=st.session_state.rand_time_periods)
        return [time_periods, frequency]

    def park_rides(self, col1, granularity: typing.Optional[list] = None):
        if self.time_assumption == "Constant":
            park_rides = pd.DataFrame({"Rides": list(self.active_rides.keys()), "Wait Times": list(self.active_rides.values())})

        elif self.time_assumption == "Dynamic":
            park_rides = pd.DataFrame({"Rides": list(self.active_rides.keys()), "Wait Times Period 1": list(self.active_rides.values())})
            for i in range(1, granularity[0]):
                park_rides[f'Wait Times Period {i+1}'] = 0
        
        col1.markdown("<h2 style='text-align: center;'>Active Rides</h2",
                            unsafe_allow_html=True, help="Feel free to add, delete, or edit the rides data")
        experimental_rides_df = col1.experimental_data_editor(park_rides, num_rows="fixed")

        return experimental_rides_df

    def required_constraints(self, rides):
        st.sidebar.markdown("<h2 style='text-align: center;'>Required Constraint</h2", unsafe_allow_html=True, help="This constraint must be set to have any meaningful results")
        if st.session_state.optimization_problem == "Maximize Rides":
            max_time_slider = st.sidebar.slider("Maximum Time Constraint", max_value=300, help="What is the maximum total amount of time you'd like to spend waiting for rides?")
            min_total_rides_slider = None
        elif st.session_state.optimization_problem == "Minimize Time":
            min_total_rides_slider = st.sidebar.slider("Minimum Number of Total Rides Constraint", max_value=5*len(rides.Rides), help="What is the minimum total number of rides you'd like to go on?")
            max_time_slider = None
        return [max_time_slider, min_total_rides_slider]

    def optional_constraints(self, rides,  required_constraints):
        st.sidebar.markdown("<h2 style='text-align: center;'>Optional Constraints</h2", unsafe_allow_html=True, help="These constraints are optional, but make the optimization much more interesting")
        required_rides = st.sidebar.multiselect("Required Rides", options=[i for i in rides.Rides], help="Which rides would you like to go on at least once?")

        avoid_rides = st.sidebar.multiselect("Avoid Rides", options=[i for i in rides.Rides], help="Which rides would you like to avoid entirely?")

        helper.require_avoid_contradiction(required_rides, avoid_rides)

        min_distinct_rides_slider = st.sidebar.slider("Minimum Distinct Rides", min_value=1, max_value=len(rides.Rides), help="What is the minimum number of distinct rides you'd like to go on?")

        max_ride_repeats_slider = st.sidebar.slider("Maximum Ride Repeats", min_value=1, max_value=50, value=5, help="What is the maximum number of times you'd like to ride any single ride?")

        if st.session_state.optimization_problem == "Minimize Time":
            helper.max_ride_repeats_contradiction(required_constraints[1], max_ride_repeats_slider, len(rides.Rides))
        
        user_preferences=up.UserPreferences(
            required_rides,
            avoid_rides,
            min_distinct_rides_slider,
            max_ride_repeats_slider,
            required_constraints[0],
            required_constraints[1]
            )
        
        user_preferences.convert_empty_data_types()
        return user_preferences

    def optimize(self, col2, rides, user_preferences, granularity):
        global optimize_data
        if self.time_assumption == "Constant":
            optimize_data = ct.OptimizeConstant(
                all_rides=rides.iloc[:, 0].tolist(),
                wait_times=rides.iloc[:, 1].tolist(),
                user_preferences=user_preferences 
                )
        elif self.time_assumption == "Dynamic":
            wait_times_lists = []
            for i in range(1, granularity[0]+1):
                wait_times_lists.append(rides.iloc[:, i].tolist(),)

            wait_times = {}
            for i in range(1, granularity[0]+1):
                wait_times.update({i: wait_times_lists[i-1]})

            optimize_data = dt.OptimizeDynamic(
                all_rides=rides.iloc[:, 0].tolist(),
                time_steps=granularity[0],
                frequency=granularity[1],
                wait_times=wait_times,
                user_preferences=user_preferences 
                )    
            
        ride_weights = optimize_data.set_ride_weights()

        col2.markdown("<h2 style='text-align: center;'>Optimal Results</h2", unsafe_allow_html=True, help="The 'Values' represent the number of times to go on a given ride")
        if st.session_state.optimization_problem == "Maximize Rides":
            results = optimize_data.maximize_rides(ride_weights)
        elif st.session_state.optimization_problem == "Minimize Time":
            results = optimize_data.minimize_time(ride_weights)

        if self.time_assumption == "Constant":
            try:
                ride_values = pd.DataFrame({"Rides": list(results.keys()), "Values": list(results.values())})
                col2.dataframe(ride_values)
            except:
                st.error(body="No feasible solution. If this is a stand-alone error message, consider increasing the max time constraint")
            
        elif self.time_assumption == "Dynamic":
            ride_values = pd.DataFrame({"Rides": list(rides.Rides)})
            categorized_results = {}
            for key, value in results.items():
                index = key[1]
                if index not in categorized_results:
                    categorized_results[index] = {}
                categorized_results[index][key] = value

            # Put the categorized data into a list of dicts; one for each time period
            time_period_results = []
            for time_step in range(1, granularity[0]+1):
                rides = list(categorized_results[time_step].keys())
                values = list(categorized_results[time_step].values())
                # Isolate the rides from the time periods
                isolated_rides = [ride[0] for ride in rides]
                time_period_results.append(dict(zip(isolated_rides, values)))
            for i in range(len(time_period_results)):
                ride_values[f'Results at Time Period {i+1}'] = list(time_period_results[i].values())
            col2.dataframe(ride_values)
