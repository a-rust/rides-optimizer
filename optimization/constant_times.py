import pulp
import user_preferences as up

''' 
This file considers the optimization problems assuming constant wait and ride times
'''

class OptimizeConstant():
    def __init__(self, all_rides: list, wait_times: list, ride_times: list, user_preferences: up.UserPreferences) -> None:
        self.all_rides = all_rides
        self.wait_times = wait_times
        self.ride_times = ride_times
        self.required_rides = user_preferences.required_rides
        self.avoid_rides = user_preferences.avoid_rides
        self.min_distinct_rides = user_preferences.min_distinct_rides
        self.max_time = user_preferences.max_time
        self.max_ride_repeats = user_preferences.max_ride_repeats
        self.min_total_rides = user_preferences.min_total_rides
