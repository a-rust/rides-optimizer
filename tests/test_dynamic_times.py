import optimization.dynamic_times as dt
import optimization.user_preferences as up

rides = ['a', 'b', 'c']
time_steps = 2
frequency = 100
# For the first period, the wait times for rides 'a', 'b', 'c' are 2, 4, 6, respectively, etc.
wait_times = {1: [2, 4, 6], 2: [5, 3, 7]}

def test_set_ride_weights():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=None, min_distinct_rides=None, max_ride_repeats=None, max_time=None, min_total_rides=None)
    park = dt.OptimizeDynamic(all_rides=rides, time_steps=time_steps, frequency=frequency, wait_times=wait_times, user_preferences=user_preferences)
    assert park.set_ride_weights() == {'a': [2, 5], 'b': [4, 3], 'c': [6, 7]}

def test_maximize_no_preferences():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=None, min_distinct_rides=None, max_ride_repeats=None, max_time=200, min_total_rides=None)
    park = dt.OptimizeDynamic(all_rides=rides, time_steps=time_steps, frequency=frequency, wait_times=wait_times, user_preferences=user_preferences)
    ride_weights = park.set_ride_weights()
    # Given a frequency of 100 (i.e., each time step lasts 100 units), it is optimal to ride 'a' 50 times in the first time step, and 'b' 33 times in the second time step. With additional preferences (like max ride repeats), the problem will become more interesting
    assert park.maximize_rides(ride_weights) == {('a', 1): 50.0, ('a', 2): 0.0, ('b', 1): 0.0, ('b', 2): 33.0, ('c', 1): 0.0, ('c', 2): 0.0}

def test_maximize_with_required():
    user_preferences = up.UserPreferences(required_rides=['c'], avoid_rides=None, min_distinct_rides=None, max_ride_repeats=None, max_time=200, min_total_rides=None)
    park = dt.OptimizeDynamic(all_rides=rides, time_steps=time_steps, frequency=frequency, wait_times=wait_times, user_preferences=user_preferences)
    ride_weights = park.set_ride_weights()
    # Since we require ride 'c' at least once, then it must be the case that the sum of ride_(c, j) >= 1 for all time steps j
    #   - In this case, taking away 2 units from 'a' in time step b to free up space for one unit of 'c' leads to the optimal solution
    assert park.maximize_rides(ride_weights) == {('a', 1): 50.0, ('a', 2): 0.0, ('b', 1): 0.0, ('b', 2): 31.0, ('c', 1): 0.0, ('c', 2): 1.0}

def test_maximize_with_avoid():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=['a'], min_distinct_rides=None, max_ride_repeats=None, max_time=200, min_total_rides=None)
    park = dt.OptimizeDynamic(all_rides=rides, time_steps=time_steps, frequency=frequency, wait_times=wait_times, user_preferences=user_preferences)
    ride_weights = park.set_ride_weights()
    # Since we avoid ride 'a' all together, then it must be the case that the sum of ride_(a, j) = 0 for all time steps j
    #   - In this case, 'b' is the next best option to allocate all the space to in time step 1, and time step 2 remains unchanged
    assert park.maximize_rides(ride_weights) == {('a', 1): 0.0, ('a', 2): 0.0, ('b', 1): 25.0, ('b', 2): 33.0, ('c', 1): 0.0, ('c', 2): 0.0}

def test_maximize_with_max_ride_repeat_constraint():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=None, min_distinct_rides=None, max_ride_repeats=10, max_time=200, min_total_rides=None)
    park = dt.OptimizeDynamic(all_rides=rides, time_steps=time_steps, wait_times=wait_times, frequency=frequency,  user_preferences=user_preferences)
    ride_weights = park.set_ride_weights()
    # Since we set a max ride repeat constraint of 10, then it must be the case that ('a', 1)+('a', 2) <= 10, ('b', 1)+('b', 2) <= 10, and ('c', 1)+('c', 2) <= 10
    #   - In this case, we can max out every ride (over both time periods)
    assert park.maximize_rides(ride_weights) == {('a', 1): 0.0, ('a', 2): 10.0, ('b', 1): 0.0, ('b', 2): 10.0, ('c', 1): 10.0, ('c', 2): 0.0}

def test_maximize_with_min_distinct_rides_constraint():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=None, min_distinct_rides=3, max_ride_repeats=None, max_time=200, min_total_rides=None)
    park = dt.OptimizeDynamic(all_rides=rides, time_steps=time_steps, frequency=frequency, wait_times=wait_times,  user_preferences=user_preferences)
    ride_weights = park.set_ride_weights()
    # Since we set the min distinct rides constraint to 3, then 'a', 'b', and 'c' must be rode at least once (over both time steps)
    #   - In this case, 'c' is cheaper in time step 2, and it is thus optimal to allocate space for one unit of 'c' from 2 units of 'b' in time step 2
    assert park.maximize_rides(ride_weights) == {('a', 1): 50.0, ('a', 2): 0.0, ('b', 1): 0.0, ('b', 2): 31.0, ('c', 1): 0.0, ('c', 2): 1.0}

def test_minimize_no_preferences():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=None, min_distinct_rides=None, max_ride_repeats=None, max_time=None, min_total_rides=30)
    park = dt.OptimizeDynamic(all_rides=rides, time_steps=time_steps, frequency=frequency, wait_times=wait_times, user_preferences=user_preferences)
    ride_weights = park.set_ride_weights()
    # Since we set the min total rides constraint to 30, and since 'a' in time step 1 and 'b' in time step 2 are tied for the lowest weights, then it would be optimal to set ('a', 1) = 30 and everything else to 0, or to set ('b', 2) = 30 and everything else to 0, or to use any combination of non-zero values for ('a', 1) and ('b', 2) and set everything else to 0
    assert park.minimize_time(ride_weights) == {('a', 1): 30.0, ('a', 2): 0.0, ('b', 1): 0.0, ('b', 2): 0.0, ('c', 1): 0.0, ('c', 2): 0.0}

def test_minimize_min_distinct_rides_avoid_contradiction():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=['a', 'b'], min_distinct_rides=2, max_ride_repeats=None, max_time=None, min_total_rides=30)
    park = dt.OptimizeDynamic(all_rides=rides, time_steps=time_steps, frequency=frequency, wait_times=wait_times, user_preferences=user_preferences)
    ride_weights = park.set_ride_weights()
    # Since there are only 3 distinct rides in total, then avoiding 2 of them ('a' and 'b'), means we only have 1 distinct ride left, 'c'. And requiring to go on at least 2 distinct rides with the only option being 'c' leads to an infeasible solution due to a preference/constraint contradiction
    assert park.minimize_time(ride_weights) == None
