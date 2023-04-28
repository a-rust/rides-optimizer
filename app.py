import streamlit as st
import optimization.user_preferences as up
import optimization.constant_times as ct


def define_problem():
    st.markdown("<h1 style='text-align: center;'>Demo</h1", unsafe_allow_html=True)
    time_assumption = st.selectbox("Please select the time assumptions to be used", ("Constant", "Dynamic"))
    optimization_problem = st.selectbox("Please choose which optimization problem you'd like to solve", ("Maximize Rides", "Minimize Time"))
    if optimization_problem not in st.session_state:
        st.session_state.optimization_problem = optimization_problem

define_problem()
