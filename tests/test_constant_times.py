import optimization.constant_times as ct
import optimization.user_preferences as up

# Example
rides = ['a', 'b', 'c']
wait_times = [2, 4, 6]
ride_times = [5, 2, 4]

# Test for setting the ride weights
def test_set_ride_weights():
    user_preferences = up.UserPreferences(required_rides=['a'], avoid_rides=['b'], min_distinct_rides=None, max_ride_repeats=None, max_time=None, min_total_rides=None)
    park = ct.OptimizeConstant(rides, wait_times, ride_times, user_preferences)
    # The ride weight of i is the wait time of i plus the ride time of i
    assert park.set_ride_weights() == {'a': 7, 'b': 6, 'c': 10}


# Test for maximizing the number of edges with a max time constraint
def test_maximize_rides_with_max_time():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=None, min_distinct_rides=3, max_ride_repeats=None, max_time=20, min_total_rides=None)
    park = ct.OptimizeConstant(rides, wait_times, ride_times, user_preferences)
    ride_weights = park.set_ride_weights()
    # Choosing to ride b 3 times is optimal given max_time = 20
    assert park.maximize_rides(ride_weights) == {'a': 0.0, 'b': 3.0, 'c': 0.0}
