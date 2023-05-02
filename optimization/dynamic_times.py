import pulp
import user_preferences as up

''' 
This file considers the optimization problems assuming dynamic wait and ride times.
Also assumes that these changing times are known beforehand
'''

class OptimizeDynamic():
    def __init__(self, all_rides: list, time_steps: int, wait_times: dict, ride_times: dict, user_preferences: up.UserPreferences) -> None:
        self.all_rides = all_rides
        self.time_steps = time_steps
        self.wait_times = wait_times
        self.ride_times = ride_times
        self.required_rides = user_preferences.required_rides
        self.avoid_rides = user_preferences.avoid_rides
        self.require_and_avoid = user_preferences.require_and_avoid_rides()
        self.min_distinct_rides = user_preferences.min_distinct_rides
        self.max_time = user_preferences.max_time
        self.max_ride_repeats = user_preferences.max_ride_repeats
        self.min_total_rides = user_preferences.min_total_rides


    # Returns a dict where the keys are ride names, and the values are a list of total time (where each index represents the total time at each time step)
    #   - Example: {a: [10, 15], b: [12, 13]} implies that the total times of rides a, b at the first time step are 10, 12, respectively, and the total times of rides of a, b at the second time step are 15, 13, respectively  
    def set_ride_weights(self) -> dict:
        return {self.all_rides[i]: [self.wait_times.get(j)[i] + self.ride_times.get(j)[i] for j in range(1, self.time_steps+1)] for i in range(len(self.all_rides)) for j in range(1, self.time_steps)}
