import streamlit as st
import numpy as np
import pandas as pd
import random
import optimization.user_preferences as up
import optimization.constant_times as ct


def define_problem():
    st.markdown("<h1 style='text-align: center;'>Demo</h1", unsafe_allow_html=True)

    time_assumption = st.selectbox("Please select the time assumptions to be used", ("Constant", "Dynamic"))

    optimization_problem = st.selectbox("Please choose which optimization problem you'd like to solve", ("Maximize Rides", "Minimize Time"))

    if optimization_problem not in st.session_state:
        st.session_state.optimization_problem = optimization_problem
    
    # Have to create empty side columns to keep button centered
    empty_col1, btn_col2, empty_col3 = st.columns((1, 1, 1))
    randomize_data_btn = btn_col2.button("Randomize Data")
    if randomize_data_btn:
        del st.session_state.rides
        
    ride_data_col1, ride_data_col2 = st.columns((1, 1))
    random_rides_data(ride_data_col1, ride_data_col2)
    random_constraints_data(ride_data_col1, ride_data_col2)

def random_rides_data(ride_data_col1, ride_data_col2):
    rides_col1 = [f'Ride_{i}' for i in range(1, 6)]
    rides_col2 = np.random.randint(low=0, high=10, size=5)
    rides_col3 = np.random.randint(low=0, high=10, size=5)

    rides = pd.DataFrame({"Rides": rides_col1, "Wait Times": rides_col2, "Ride Times": rides_col3})

    if "rides" not in st.session_state:
        st.session_state.rides = rides

    ride_data_col1.markdown("<h2 style='text-align: center;'>Rides</h2", unsafe_allow_html=True)

    experimental_rides_df = ride_data_col1.experimental_data_editor(st.session_state.rides, num_rows="dynamic")

    if experimental_rides_df not in st.session_state:
        st.session_state.experimental_rides_df = experimental_rides_df


def random_constraints_data(ride_data_col1, ride_data_col2):
    ride_data_col2.markdown("<h2 style='text-align: center;'>Required Constraints</h2", unsafe_allow_html=True)
    if st.session_state.optimization_problem == "Maximize Rides":
        max_time_slider = ride_data_col2.slider("Maximum Time Constraint", value=random.randint(0, 300))
    else:
        max_time_slider = None
    if st.session_state.optimization_problem == "Minimize Time":
        min_total_rides_slider = ride_data_col2.slider("Minimum Number of Rides Constraint", value=random.randint(0, 300))
    else:
        min_total_rides_slider = None


define_problem()
