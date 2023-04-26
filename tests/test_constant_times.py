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
    # The ride weight of ride i is the wait time of ride i plus the ride time of ride i
    assert park.set_ride_weights() == {'a': 7, 'b': 6, 'c': 10}

# Test for maximizing the number of rides with a max time constraint
def test_maximize_rides_with_max_time():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=None, min_distinct_rides=None, max_ride_repeats=None, max_time=20, min_total_rides=None)
    park = ct.OptimizeConstant(rides, wait_times, ride_times, user_preferences)
    ride_weights = park.set_ride_weights()
    # Choosing to ride 'b' 3 times is optimal given max_time = 20
    assert park.maximize_rides(ride_weights) == {'a': 0.0, 'b': 3.0, 'c': 0.0}

# Test for maximizing the number of rides with no max time constraint
def test_maximize_rides_with_no_max_time():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=None, min_distinct_rides=None, max_ride_repeats=None, max_time=None, min_total_rides=None)
    park = ct.OptimizeConstant(rides, wait_times, ride_times, user_preferences)
    ride_weights = park.set_ride_weights()
    # The solution is unbounded if no max_time_constraint, and so maximize_rides should return None
    assert park.maximize_rides(ride_weights) == None

# Test for maximizing the number of rides with max ride repeats constraint
def test_maximize_rides_with_max_ride_repeats():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=None, min_distinct_rides=None, max_ride_repeats=2, max_time=30, min_total_rides=None)
    park = ct.OptimizeConstant(rides, wait_times, ride_times, user_preferences)
    ride_weights = park.set_ride_weights()
    # The solution is unbounded if no max_time_constraint, and so maximize_rides should return None
    assert park.maximize_rides(ride_weights) == {'a': 2.0, 'b': 2.0, 'c': 0.0}

# Test for maximizing the number of rides with no max ride repeats constraint
def test_maximize_rides_with_no_max_ride_repeats():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=None, min_distinct_rides=None, max_ride_repeats=None, max_time=30, min_total_rides=None)
    park = ct.OptimizeConstant(rides, wait_times, ride_times, user_preferences)
    ride_weights = park.set_ride_weights()
    # If no max ride repeats, all of the space will be go to 'b', as the weight of 'b' is less than the weights of 'a' and 'c'
    assert park.maximize_rides(ride_weights) == {'a': 0.0, 'b': 5.0, 'c': 0.0}

# Test for maximizing the number of rides with required rides constraint
def test_maximize_rides_with_required_rides():
    user_preferences = up.UserPreferences(required_rides=['a'], avoid_rides=None, min_distinct_rides=None, max_ride_repeats=None, max_time=30, min_total_rides=None)
    park = ct.OptimizeConstant(rides, wait_times, ride_times, user_preferences)
    ride_weights = park.set_ride_weights()
    # Requiring to go on ride 'a' at least once will assign 1 to 'a', and utilize the rest of the space with 'b', as the weight of 'b' is less than the weights of 'a' and 'c'
    assert park.maximize_rides(ride_weights) == {'a': 1.0, 'b': 3.0, 'c': 0.0}

# Test for maximizing the number of rides with avoid rides constraint
def test_maximize_rides_with_avoid_rides():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=['b'], min_distinct_rides=None, max_ride_repeats=None, max_time=30, min_total_rides=None)
    park = ct.OptimizeConstant(rides, wait_times, ride_times, user_preferences)
    ride_weights = park.set_ride_weights()
    # Avoiding 'b' entirely will result in utilizing 'a' for all of the space, as the weight of 'a' is less than the weight of 'c'
    assert park.maximize_rides(ride_weights) == {'a': 4.0, 'b': 0.0, 'c': 0.0}
    
# Test for maximizing the number of rides with no required rides or avoid rides constraints
def test_maximize_rides_with_no_required_or_avoid_rides():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=None, min_distinct_rides=None, max_ride_repeats=None, max_time=30, min_total_rides=None)
    park = ct.OptimizeConstant(rides, wait_times, ride_times, user_preferences)
    ride_weights = park.set_ride_weights()
    # Not specifying any required rides will result in utilizing all of the space with 'b', as the weight of 'b' is less than the weights of 'a' and 'c'
    assert park.maximize_rides(ride_weights) == {'a': 0.0, 'b': 5.0, 'c': 0.0}
    
# Test for enforcing that a user cannot both require and avoid the same ride
def test_maximize_rides_with_same_required_avoid_rides():
    user_preferences = up.UserPreferences(required_rides=['a'], avoid_rides=['a'], min_distinct_rides=None, max_ride_repeats=None, max_time=30, min_total_rides=None)
    park = ct.OptimizeConstant(rides, wait_times, ride_times, user_preferences)
    ride_weights = park.set_ride_weights()
    # Cannot require and avoid 'a' at the same time
    assert park.maximize_rides(ride_weights) == None
