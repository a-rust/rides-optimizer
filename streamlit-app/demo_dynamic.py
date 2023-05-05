import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import floor
import random
import helper
import optimization.user_preferences as up
import optimization.dynamic_times as dt

def main():
    optimization_problem = st.selectbox("Please choose which optimization problem you'd like to solve", ("Maximize Rides", "Minimize Time"), help="Do you want to maximize the total number of rides to go on, or minimize the total amount of time spent at the park?")
    if optimization_problem not in st.session_state:
        st.session_state.optimization_problem = optimization_problem
    
    empty_col1, btn_col2, empty_col3 = st.columns((1, 1, 1))
    randomize_data_btn = btn_col2.button("Randomize Data")
    if randomize_data_btn:
        del st.session_state.rand_frequency
        del st.session_state.rand_park_open_time
        del st.session_state.rides_dynamic
        if st.session_state.optimization_problem == "Maximize Rides":
            del st.session_state.rand_max_time_slider_dynamic
        if st.session_state.optimization_problem == "Minimize Time":
            del st.session_state.rand_min_total_rides_slider_dynamic
        del st.session_state.rand_required_rides_dynamic
        del st.session_state.rand_avoid_rides_dynamic 
        del st.session_state.rand_min_distinct_rides_dynamic
        del st.session_state.rand_max_ride_repeats_dynamic
            
    ride_data_col1, result_col2 = st.columns((1, 1))
    time_steps = granularity()
    rides_dynamic = demo_rides(time_steps, ride_data_col1)
    required_constraints = random_required_constraints_data(rides_dynamic)
    user_preferences = random_optional_constraints_data(rides_dynamic, required_constraints)
    optimize(time_steps, rides_dynamic, user_preferences, result_col2)


def granularity():
    st.sidebar.markdown("<h2 style='text-align: center;'>Time Updates</h2", unsafe_allow_html=True, help="Control the time changes")
    rand_frequency = 10*random.randint(2, 10)
    if "rand_frequency" not in st.session_state:
        st.session_state.rand_frequency = rand_frequency
    frequency = st.sidebar.slider("Time Change Frequency (minutes)", min_value=20, max_value=100,  value=st.session_state.rand_frequency, key="frequency_slider", help="How often will the wait/rides times change?")
    rand_park_open_time = 10*random.randint(20, 100)
    if "rand_park_open_time" not in st.session_state:
        st.session_state.rand_park_open_time = rand_park_open_time
    park_open_mins = st.sidebar.slider("How long will the park open for (minutes)?", min_value=100, max_value=1000, value=st.session_state.rand_park_open_time)
    time_steps = floor(park_open_mins / frequency) + 1
    return time_steps

def demo_rides(time_steps, ride_data_col1):

    rides_col1 = [f'Ride_{i}' for i in range(1, 8)]
    rides_dynamic = pd.DataFrame({'Rides': rides_col1})

    rand_wait_times = []
    rand_ride_times = []
    for i in range(time_steps):
        rand_wait_times.append(np.random.randint(low=0, high=10, size=7))
        rand_ride_times.append(np.random.randint(low=0, high=10, size=7))
    for i in range(1, time_steps):
        rides_dynamic[f'Wait Times Period {i}'] = rand_wait_times[i]
        rides_dynamic[f'Ride Times Period {i}'] = rand_ride_times[i]

    if "rides_dynamic" not in st.session_state:
        st.session_state.rides_dynamic = rides_dynamic
    
    ride_data_col1.markdown("<h2 style='text-align: center;'>Rides</h2", unsafe_allow_html=True)

    experimental_rides_dynamic_df = ride_data_col1.experimental_data_editor(st.session_state.rides_dynamic, num_rows="dynamic")
    return experimental_rides_dynamic_df
    

def random_required_constraints_data(rides_dynamic):
    st.sidebar.markdown("<h2 style='text-align: center;'>Required Constraint</h2", unsafe_allow_html=True, help="This constraint must be set to have any meaningful results")
    if st.session_state.optimization_problem == "Maximize Rides":
        # Artificial lower bound on max time constraint to avoid infeasibility of randomly generated data
        rand_max_time_slider_dynamic = random.randint(10*len(rides_dynamic.Rides), 300)
        if "rand_max_time_slider_dynamic" not in st.session_state:
            st.session_state.rand_max_time_slider_dynamic = rand_max_time_slider_dynamic
        max_time_slider = st.sidebar.slider("Maximum Time Constraint", max_value=300, value=st.session_state.rand_max_time_slider_dynamic, help="What is the maximum total amount of time you'd like to spend waiting and riding rides?")
    else:
        max_time_slider = None
    if st.session_state.optimization_problem == "Minimize Time":
        rand_min_total_rides_slider_dynamic = random.randint(0, 10*len(rides_dynamic.Rides))
        if "rand_min_total_rides_slider_dynamic" not in st.session_state:
            st.session_state.rand_min_total_rides_slider_dynamic = rand_min_total_rides_slider_dynamic
        min_total_rides_slider = st.sidebar.slider("Minimum Number of Total Rides Constraint", max_value=5*len(rides_dynamic.Rides), value=st.session_state.rand_min_total_rides_slider_dynamic, help="What is the minimum total number of rides you'd like to go on?")
    else:
        min_total_rides_slider = None

    return [max_time_slider, min_total_rides_slider]

def random_optional_constraints_data(rides_dynamic, required_constraints):
    st.sidebar.markdown("<h2 style='text-align: center;'>Optional Constraints</h2", unsafe_allow_html=True, help="These constraints are optional, but make the optimization much more interesting")
    rand_required_rides_dynamic = random.choice(rides_dynamic.Rides)
    if "rand_required_rides_dynamic" not in st.session_state:
        st.session_state.rand_required_rides_dynamic = rand_required_rides_dynamic
    required_rides = st.sidebar.multiselect("Required Rides",  options=[i for i in rides_dynamic.Rides], default=st.session_state.rand_required_rides_dynamic, help="Which rides would you like to go on at least once?")

    # Prevent random avoid ride to be distinct from random required ride
    rand_avoid_rides_dynamic = random.choice(list(set(rides_dynamic.Rides).difference(set(required_rides))))
    if "rand_avoid_rides_dynamic" not in st.session_state:
        st.session_state.rand_avoid_rides_dynamic = rand_avoid_rides_dynamic
    avoid_rides = st.sidebar.multiselect("Avoid Rides",  options=[i for i in rides_dynamic.Rides], default=st.session_state.rand_avoid_rides_dynamic, help="Which rides would you like to avoid entirely?")

    # Prevent user from requiring and avoiding the same ride(s)
    helper.require_avoid_contradiction(required_rides, avoid_rides)

    # The rand_min_distinct_rides should not be larger than either (# of rides - # of avoided rides) or the min total rides (in the case of a minimization problem)
    if required_constraints[1] != None:
        rand_min_distinct_rides_dynamic = random.randint(0, min(len(rides_dynamic.Rides) - len(avoid_rides), required_constraints[1]))
    else: 
        rand_min_distinct_rides_dynamic = random.randint(1, len(rides_dynamic.Rides) - len(avoid_rides))
    if "rand_min_distinct_rides_dynamic" not in st.session_state:
        st.session_state.rand_min_distinct_rides_dynamic = rand_min_distinct_rides_dynamic
    min_distinct_rides_slider = st.sidebar.slider("Minimum Distinct Rides", min_value=1, max_value=len(rides_dynamic.Rides), value=st.session_state.rand_min_distinct_rides_dynamic, help="What is the minimum number of distinct rides you'd like to go on?")

    helper.min_distinct_rides_contradiction(min_distinct_rides_slider, len(rides_dynamic.Rides), len(avoid_rides))

    rand_max_ride_repeats_dynamic = random.randint(1, len(rides_dynamic.Rides))
    if "rand_max_ride_repeats_dynamic" not in st.session_state:
        st.session_state.rand_max_ride_repeats_dynamic = rand_max_ride_repeats_dynamic
    max_ride_repeats_slider = st.sidebar.slider("Maximum Ride Repeats", min_value=1, value=st.session_state.rand_max_ride_repeats_dynamic, help="What is the maximum number of times you'd like to ride any single ride?")

    if st.session_state.optimization_problem == "Minimize Time":
        helper.max_ride_repeats_contradiction(required_constraints[1], max_ride_repeats_slider, len(rides_dynamic.Rides))

    user_preferences=up.UserPreferences(
        required_rides,
        avoid_rides,
        min_distinct_rides_slider,
        max_ride_repeats_slider,
        {1: required_constraints[0]},
        required_constraints[1]
        ) 

    user_preferences.convert_empty_data_types()
    return user_preferences

def optimize(time_steps, rides_dynamic, user_preferences, result_col2):
    wait_times_lists = []
    ride_times_lists = []
    for i in range(1, 2*time_steps-1):
        if i % 2 == 0:
            ride_times_lists.append(rides_dynamic.iloc[:, i].tolist(),)
        else:
            wait_times_lists.append(rides_dynamic.iloc[:, i].tolist(),)

    wait_times = {}
    ride_times = {}
    for i in range(1, time_steps):
        wait_times.update({i: wait_times_lists[i-1]})
        ride_times.update({i: ride_times_lists[i-1]})

    optimize_data = dt.OptimizeDynamic(
        all_rides=rides_dynamic.iloc[:, 0].tolist(),
        time_steps=time_steps,
        wait_times=wait_times,
        ride_times=ride_times,
        user_preferences=user_preferences 
        )
