import typing
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
    def __init__(self, required_rides: typing.Optional[list] = None, avoid_rides: typing.Optional[list] = None, min_distinct_rides: typing.Optional[list] = None, max_ride_repeats: typing.Optional[list] = None, max_time: typing.Optional[int] = None, min_total_rides: typing.Optional[int] = None):
        self.required_rides = required_rides
        self.avoid_rides = avoid_rides
        self.min_distinct_rides = min_distinct_rides
        self.max_ride_repeats = max_ride_repeats
        self.max_time = max_time
        self.min_total_rides = min_total_rides

    # Converts empty data types to None
    def convert_empty_data_types(self):
        if self.required_rides == []:
            self.required_rides = None
        if self.avoid_rides == []:
            self.avoid_rides = None
        if self.min_distinct_rides == 0:
            self.min_distinct_rides = None
        if self.max_ride_repeats == 0:
            self.max_ride_repeats = None

    # Returns a boolean as to whether any rides are being both required and avoided at the same time
    def require_and_avoid_rides(self) -> bool:
        if self.required_rides != None and self.avoid_rides != None:
            if len(set(self.required_rides).intersection(set(self.avoid_rides))) > 0:
                return True
            else:
                return False
