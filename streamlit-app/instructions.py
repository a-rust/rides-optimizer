import streamlit as st

def guide():
    with st.expander("What is this?🎢"):
        st.markdown("Whenever you go to an amusement park, how often do you think about the wait times for a given ride?")
        st.markdown("This app uses integer programming to optimize which set of rides to go on (and how many times), while also considering the ride wait times. Informally, this app solves the following 2 generalized optimization problems:")
        st.markdown("1. Maximize the total number of rides to go on, given some maximum amount of time you'd like to spend waiting in line for rides")
        st.markdown("2. Minimize the total amount of time spent waiting in line for rides, given some minimum number of total rides you'd like to go on")
        st.markdown("These optimization problems may seem trivial. However, this app also considers personal preferences such as choosing the rides to require/avoid in the optimal solution, choosing the minimum number of distinct rides in the optimal solution, choosing the maximum number of times a ride can be rode in the optimal solution, etc.")
        st.markdown("**One major assumption to consider is how to handle the wait times of the rides**")
        st.markdown("* In general, the wait times could either be constant, or dynamically changing throughout the day. Although the latter is more likely, it is still interesting to consider both cases")
        st.markdown("* For constant wait times, the optimization problem is essentially an instance of the knapsack problem, where the wait time of each ride is its weight")
        st.markdown("* For dynamic wait times, there are 'time periods', which represent the intervals for each set of (changing) wait times. It's assumed that each time period lasts the same amount of time. The idea is to then consider the wait times of each ride over each time period as a unique individual item used within an instance of the knapsack problem.")
        st.markdown("**These optimization problems can only be solved if the wait times of each ride (at each time period) are known beforehand**")
        st.markdown("* There exist external API's like [ThemeParks](https://themeparks.wiki/) that offer real-time data for amusement park rides, such as ride wait times")
        st.markdown("* This means that the optimal solution for the constant time assumption model should be correct (at least in theory)")
        st.markdown("* For the dynamic wait times assumption, it's quite difficult to predict what the wait times will be at each (future) time period. However, there could very well be a follow-up project that involves predicting future wait times")
