'''
This class will be associated with user preferences, which will ultimately define the constraints of the mixed integer programming problems.
For now, we only consider the following user preferences (will update later):
- Which rides the user wants to go on at least once
- Which rides the user doesn't want to go on at all
- The minimum number of distinct rides to go on at least once
- The maximum number of times a single ride can be repeated
- The maximum amount of time that can be spent at the park waiting for rides + actually riding them
    - Only applies to the maximization problem
- The minimum number of total rides to go on
    - Only applies to the minimization problem
'''

class UserPreferences():
    def __init__(self, required_rides: list | None, avoid_rides: list | None, min_distinct_rides: list | None, max_ride_repeats: list | None, max_time: int | None, min_total_rides: int | None):
        self.required_rides = required_rides
        self.avoid_rides = avoid_rides
        self.min_distinct_rides = min_distinct_rides
        self.max_ride_repeats = max_ride_repeats
        self.max_time = max_time
        self.min_total_rides = min_total_rides
