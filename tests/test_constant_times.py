import optimization.constant_times as ct
import optimization.user_preferences as up

# Example
rides = ['a', 'b', 'c']
wait_times = [2, 4, 6]
ride_times = [5, 2, 4]

# -------------------
# Setter method tests
# -------------------

# Test for setting the ride weights
def test_set_ride_weights():
    user_preferences = up.UserPreferences(required_rides=['a'], avoid_rides=['b'], min_distinct_rides=None, max_ride_repeats=None, max_time=None, min_total_rides=None)
    park = ct.OptimizeConstant(rides, wait_times, ride_times, user_preferences)
    # The ride weight of ride i is the wait time of ride i plus the ride time of ride i
    assert park.set_ride_weights() == {'a': 7, 'b': 6, 'c': 10}

# -------------------------
# Maximization method tests
# -------------------------

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

# Test for maximizing the number of rides with min distinct rides constraint
def test_maximize_rides_with_min_distinct_rides():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=None, min_distinct_rides=3, max_ride_repeats=None, max_time=30, min_total_rides=None)
    park = ct.OptimizeConstant(rides, wait_times, ride_times, user_preferences)
    ride_weights = park.set_ride_weights()
    # We require all 3 distinct rides, which means we must ride rides 'a', 'b', 'c' at least once. Their summed weight is 23, which means that there is 30-23=7 extra space left over, which fits one more value of 'b'
    assert park.maximize_rides(ride_weights) == {'a': 1.0, 'b': 2.0, 'c': 1.0}

# -------------------------
# Minimization method tests
# -------------------------

# Test for minimizing the total time with min total rides constraint
def test_minimize_time_with_min_total_rides():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=None, min_distinct_rides=None, max_ride_repeats=None, max_time=None, min_total_rides=10)
    park = ct.OptimizeConstant(rides, wait_times, ride_times, user_preferences)
    ride_weights = park.set_ride_weights()
    # Requiring to go on at least 10 total rides (not necessarily distinct) will result in repeating 'b' 10 times. Assigning a positive integer value to min_distinct_rides will force going on more than just 'b' 
    assert park.minimize_time(ride_weights) == {'a': 0.0, 'b': 10.0, 'c': 0.0}

# Test for minimizing the total time with no min total rides constraint
def test_minimize_time_with_no_min_total_rides():
    user_preferences = up.UserPreferences(required_rides=None, avoid_rides=None, min_distinct_rides=None, max_ride_repeats=None, max_time=None, min_total_rides=None)
    park = ct.OptimizeConstant(rides, wait_times, ride_times, user_preferences)
    ride_weights = park.set_ride_weights()
    # Not setting a min total rides will result in an optimal solution going on 0 rides, which is trivial and thus returns None 
    assert park.minimize_time(ride_weights) == None

# Test for minimizing the total time with all applicable constraints
#   - Implementation for non-required constraints are same as maximization method, which already tested
def test_minimize_time_with_all_constraints():
    user_preferences = up.UserPreferences(required_rides=['a', 'c'], avoid_rides=['b'], min_distinct_rides=None, max_ride_repeats=None, max_time=None, min_total_rides=10)
    park = ct.OptimizeConstant(rides, wait_times, ride_times, user_preferences)
    ride_weights = park.set_ride_weights()
    # Requiring to go on rides 'a' and 'c' at least once, while avoiding ride 'b' entirely, and also requiring to go on at least 10 total rides will result in going on 'a' 9 times, and going on 'c' just once, since the weight of 'a' is less than the weight of 'c'
    assert park.minimize_time(ride_weights) == {'a': 9.0, 'b': 0.0, 'c': 1.0}

# Test to check user preferences that lead to a contradiction
def test_minimize_time_contradiction():
    user_preferences = up.UserPreferences(required_rides=['a', 'c'], avoid_rides=['b'], min_distinct_rides=None, max_ride_repeats=2, max_time=None, min_total_rides=10)
    park = ct.OptimizeConstant(rides, wait_times, ride_times, user_preferences)
    ride_weights = park.set_ride_weights()
    # Setting the min total rides to be larger than the product of the size of all distinct rides and the max ride repeats leads to a contradiction
    assert park.minimize_time(ride_weights) == None