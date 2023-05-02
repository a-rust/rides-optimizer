import optimization.dynamic_times as dt
import optimization.user_preferences as up

rides = ['a', 'b', 'c']
time_steps = 2
# For the first period, the wait times for rides 'a', 'b', 'c' are 2, 4, 6, respectively, etc.
wait_times = {1: [2, 4, 6], 2: [5, 6, 7]}
ride_times = {1: [3, 5, 7], 2: [1, 2, 0]}
user_preferences = up.UserPreferences(required_rides=None, avoid_rides=None, min_distinct_rides=None, max_ride_repeats=None, max_time=None, min_total_rides=None)

def test_set_ride_weights():
    park = dt.OptimizeDynamic(all_rides=rides, time_steps=time_steps, wait_times=wait_times, ride_times=ride_times, user_preferences=user_preferences)
    assert park.set_ride_weights() == {'a': [5, 6], 'b': [9, 8], 'c': [13, 7]}
