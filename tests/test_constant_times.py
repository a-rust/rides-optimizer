import optimization.constant_times as ct
import optimization.user_preferences as up

# Example
rides = ['a', 'b', 'c']
wait_times = [2, 4, 6]
ride_times = [5, 2, 4]
user_preferences = up.UserPreferences(required_rides=['a'], avoid_rides=['b'], min_distinct_rides=None, max_ride_repeats=None, max_time=None, min_total_rides=None)

park = ct.OptimizeConstant(rides, wait_times, ride_times, user_preferences)

# Test for setting the ride weights
def test_set_ride_weights():
    # The ride weight of i is the wait time of i plus the ride time of i
    assert park.set_ride_weights() == {'a': 7, 'b': 6, 'c': 10}
