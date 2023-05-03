import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import optimization.user_preferences as up
import optimization.dynamic_times as dt

def main():
    optimization_problem = st.selectbox("Please choose which optimization problem you'd like to solve", ("Maximize Rides", "Minimize Time"), help="Do you want to maximize the total number of rides to go on, or minimize the total amount of time spent at the park?")
    if optimization_problem not in st.session_state:
        st.session_state.optimization_problem = optimization_problem
    
    empty_col1, btn_col2, empty_col3 = st.columns((1, 1, 1))
    randomize_data_btn = btn_col2.button("Randomize Data")
    if randomize_data_btn:
        del st.session_state.rand_granularity
        
    ride_data_col1, result_col2 = st.columns((1, 1))
    granularity = demo_granularity(ride_data_col1)

def demo_granularity(ride_data_col1):

    rand_granularity = random.randint(2, 5)
    if "rand_granularity" not in st.session_state:
        st.session_state.rand_granularity = rand_granularity
    granularity = st.sidebar.slider("Granularity", min_value=2, max_value=5, value=st.session_state.rand_granularity, help="How often will the wait and/or ride times change?")

    return granularity
