import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import optimization.user_preferences as up
import optimization.constant_times as ct


def set_park():
    park = st.sidebar.selectbox(label="Park", options=("Demo", "Empty for now"))
    if park == "Demo":
        demo()

def demo():
    st.markdown("<h1 style='text-align: center;'>Demo</h1", unsafe_allow_html=True)

    time_assumption = st.selectbox("Please select the time assumptions to be used", ("Constant", "Dynamic"), help="Do you want to assume constant or dynamic wait and ride times?")

    optimization_problem = st.selectbox("Please choose which optimization problem you'd like to solve", ("Maximize Rides", "Minimize Time"), help="Do you want to maximize the total number of rides to go on, or minimize the total amount of time spent at the park?")

    if optimization_problem not in st.session_state:
        st.session_state.optimization_problem = optimization_problem
    
    # Have to create empty side columns to keep button centered
    empty_col1, btn_col2, empty_col3 = st.columns((1, 1, 1))
    randomize_data_btn = btn_col2.button("Randomize Data")
    if randomize_data_btn:
        del st.session_state.rides
        if st.session_state.optimization_problem == "Maximize Rides":
            del st.session_state.rand_max_time_slider
        if st.session_state.optimization_problem == "Minimize Time":
            del st.session_state.rand_min_total_rides_slider
        del st.session_state.rand_required_rides
        del st.session_state.rand_avoid_rides
        del st.session_state.rand_min_distinct_rides
        del st.session_state.rand_max_ride_repeats
        
    ride_data_col1, result_col2 = st.columns((1, 1))
    rides = demo_random_rides_data(ride_data_col1)
    required_constraints = random_required_constraints_data()
    user_preferences = random_optional_constraints_data(rides, required_constraints)
    optimize(rides, user_preferences, result_col2)

def demo_random_rides_data(ride_data_col1):
    rides_col1 = [f'Ride_{i}' for i in range(1, 6)]
    rides_col2 = np.random.randint(low=0, high=10, size=5)
    rides_col3 = np.random.randint(low=0, high=10, size=5)

    rides = pd.DataFrame({"Rides": rides_col1, "Wait Times": rides_col2, "Ride Times": rides_col3})

    if "rides" not in st.session_state:
        st.session_state.rides = rides

    ride_data_col1.markdown("<h2 style='text-align: center;'>Rides</h2", unsafe_allow_html=True, help="Feel free to add, delete, or edit the rides data")

    experimental_rides_df = ride_data_col1.experimental_data_editor(st.session_state.rides, num_rows="dynamic", key="user_rides")

    return experimental_rides_df

def random_required_constraints_data():
    st.sidebar.markdown("<h2 style='text-align: center;'>Required Constraint</h2", unsafe_allow_html=True, help="This constraint must be set to have any meaningful results")
    if st.session_state.optimization_problem == "Maximize Rides":
        rand_max_time_slider = random.randint(0, 300)
        if "rand_max_time_slider" not in st.session_state:
            st.session_state.rand_max_time_slider = rand_max_time_slider
        max_time_slider = st.sidebar.slider("Maximum Time Constraint", value=st.session_state.rand_max_time_slider, help="What is the maximum total amount of time you'd like to spend waiting and riding rides?")
    else:
        max_time_slider = None
    if st.session_state.optimization_problem == "Minimize Time":
        rand_min_total_rides_slider = random.randint(0, 300)
        if "rand_min_total_rides_slider" not in st.session_state:
            st.session_state.rand_min_total_rides_slider = rand_min_total_rides_slider
        min_total_rides_slider = st.sidebar.slider("Minimum Number of Rides Constraint", value=st.session_state.rand_min_total_rides_slider, help="What is the minimum total number of rides you'd like to go on?")
    else:
        min_total_rides_slider = None

    return [max_time_slider, min_total_rides_slider]

def random_optional_constraints_data(rides, required_constraints):
    st.sidebar.markdown("<h2 style='text-align: center;'>Optional Constraints</h2", unsafe_allow_html=True, help="These constraints are optional, but make the optimization much more interesting")
    rand_required_rides = random.choice(rides.Rides)
    if "rand_required_rides" not in st.session_state:
        st.session_state.rand_required_rides = rand_required_rides
    required_rides = st.sidebar.multiselect("Required Rides",  options=[i for i in rides.Rides], default=st.session_state.rand_required_rides, help="Which rides would you like to go on at least once?")

    rand_avoid_rides = random.choice(rides.Rides)
    if "rand_avoid_rides" not in st.session_state:
        st.session_state.rand_avoid_rides = rand_avoid_rides
    avoid_rides = st.sidebar.multiselect("Avoid Rides",  options=[i for i in rides.Rides], default=st.session_state.rand_avoid_rides, help="Which rides would you like to avoid entirely?")

    rand_min_distinct_rides = random.randint(0, len(rides.Rides))
    if "rand_min_distinct_rides" not in st.session_state:
        st.session_state.rand_min_distinct_rides = rand_min_distinct_rides
    min_distinct_rides_slider = st.sidebar.slider("Minimum Distinct Rides", value=st.session_state.rand_min_distinct_rides, help="What is the minimum number of distinct rides you'd like to go on?")

    rand_max_ride_repeats = random.randint(0, len(rides.Rides))
    if "rand_max_ride_repeats" not in st.session_state:
        st.session_state.rand_max_ride_repeats = rand_max_ride_repeats
    max_ride_repeats_slider = st.sidebar.slider("Maximum Ride Repeats", value=st.session_state.rand_max_ride_repeats, help="What is the maximum number of times you'd like to ride any single ride?")

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

def optimize(rides, user_preferences, result_col2):
    optimize_data = ct.OptimizeConstant(
        all_rides=rides.iloc[:, 0].tolist(),
        wait_times=rides.iloc[:, 1].tolist(),
        ride_times=rides.iloc[:, 2].tolist(),
        user_preferences=user_preferences 
        )

    ride_weights = optimize_data.set_ride_weights()
    if st.session_state.optimization_problem == "Maximize Rides":
        results = optimize_data.maximize_rides(ride_weights)
    elif st.session_state.optimization_problem == "Minimize Time":
        results = optimize_data.minimize_time(ride_weights)
    result_col2.markdown("<h2 style='text-align: center;'>Results</h2", unsafe_allow_html=True, help="Watch how changing the inputs to the optimization problem affects the results. If you get an error, try and spot where certain constraints contradict each other")
    try:
        plt.bar(results.keys(), results.values())
        result_col2.pyplot(plt)
    except:
        st.error(body="No feasible solution. Please double check the constraints for any contradiction")

set_park()
