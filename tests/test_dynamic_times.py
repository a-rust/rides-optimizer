import optimization.dynamic_times as dt
import optimization.user_preferences as up

rides = ['a', 'b', 'c']
time_steps = 2
# For the first period, the wait times for rides 'a', 'b', 'c' are 2, 4, 6, respectively, etc.
wait_times = {1: [2, 4, 6], 2: [5, 3, 7]}
ride_times = {1: [3, 5, 7], 2: [1, 2, 0]}

def test_set_ride_weights():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=None, min_distinct_rides=None, max_ride_repeats=None, max_time=None, min_total_rides=None)
    park = dt.OptimizeDynamic(all_rides=rides, time_steps=time_steps, wait_times=wait_times, ride_times=ride_times, user_preferences=user_preferences)
    assert park.set_ride_weights() == {'a': [5, 6], 'b': [9, 5], 'c': [13, 7]}

def test_maximize_no_preferences():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=None, min_distinct_rides=None, max_ride_repeats=None, max_time=[100, 80], min_total_rides=None)
    park = dt.OptimizeDynamic(all_rides=rides, time_steps=time_steps, wait_times=wait_times, ride_times=ride_times, user_preferences=user_preferences)
    ride_weights = park.set_ride_weights()
    # Given a max time constraint of 100 in the first time step and a max time constraint of 80 in the second time step, it is optimal to ride 'a' 20 times in the first time step, and 'b' 16 times in the second time step. With additional preferences (like max ride repeats), the problem will become more interesting
    assert park.maximize_rides(ride_weights) == {('a', 1): 20.0, ('a', 2): 0.0, ('b', 1): 0.0, ('b', 2): 16.0, ('c', 1): 0.0, ('c', 2): 0.0}

def test_maximize_with_required():
    user_preferences = up.UserPreferences(required_rides=['c'], avoid_rides=None, min_distinct_rides=None, max_ride_repeats=None, max_time=[100, 80], min_total_rides=None)
    park = dt.OptimizeDynamic(all_rides=rides, time_steps=time_steps, wait_times=wait_times, ride_times=ride_times, user_preferences=user_preferences)
    ride_weights = park.set_ride_weights()
    # Since we require ride 'c' at least once, then it must be the case that the sum of ride_(c, j) >= 1 for all time steps j
    #   - In this case, taking away two units from 'b' in time step 2 to free up space for one unit of 'c' leads to the optimal solution
    assert park.maximize_rides(ride_weights) == {('a', 1): 20.0, ('a', 2): 0.0, ('b', 1): 0.0, ('b', 2): 14.0, ('c', 1): 0.0, ('c', 2): 1.0}

def test_maximize_with_avoid():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=['a'], min_distinct_rides=None, max_ride_repeats=None, max_time=[100, 80], min_total_rides=None)
    park = dt.OptimizeDynamic(all_rides=rides, time_steps=time_steps, wait_times=wait_times, ride_times=ride_times, user_preferences=user_preferences)
    ride_weights = park.set_ride_weights()
    # Since we avoid ride 'a' all together, then it must be the case that the sum of ride_(a, j) = 0 for all time steps j
    #   - In this case, 'b' is the next best option to allocate all the space to in time step 1, and time step 2 remains unchanged
    assert park.maximize_rides(ride_weights) == {('a', 1): 0.0, ('a', 2): 0.0, ('b', 1): 11.0, ('b', 2): 16.0, ('c', 1): 0.0, ('c', 2): 0.0}