import streamlit as st

# -----------------------
# Contradiction functions
# -----------------------

def require_avoid_contradiction(required_rides: list, avoid_rides: list):
    # Prevent user from requiring and avoiding the same ride(s)
    rides_intersection = list(set(required_rides).intersection(set(avoid_rides)))
    if rides_intersection != []:
        st.error(f"Cannot require and avoid the same rides: {rides_intersection}")

def min_distinct_rides_contradiction(num_min_distinct_rides: int, num_all_rides: int, num_avoid_rides: int):
    # Prevent user from requiring to go on X > (N - A) distinct rides, where N is the total number of distinct rides, and A is the size of the avoid rides list
    if num_all_rides < num_min_distinct_rides + num_avoid_rides:
        st.error(f"Cannot go on at least {num_min_distinct_rides} distinct rides while also avoiding {num_avoid_rides} distinct rides, given that there are only {num_all_rides} unique rides in total. Contradiction: {num_all_rides} < {num_min_distinct_rides} + {num_avoid_rides}")

def max_ride_repeats_contradiction(num_min_total_rides, num_max_ride_repeats, num_all_rides):
    # Prevent user from requiring to go on more total rides than available, given the max ride repeats constraint along with the total number of unique rides to choose from
    if num_min_total_rides > num_max_ride_repeats * num_all_rides:
        st.error(f"Cannot go on the at least {num_min_total_rides} total rides given a max ride repeat of {num_max_ride_repeats} along with only {num_all_rides} unique rides to choose from. Contradiction: {num_min_total_rides} * {num_max_ride_repeats} > {num_all_rides}")
