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
        self.require_and_avoid = user_preferences.require_and_avoid_rides()
        self.min_distinct_rides = user_preferences.min_distinct_rides
        self.max_time = user_preferences.max_time
        self.max_ride_repeats = user_preferences.max_ride_repeats
        self.min_total_rides = user_preferences.min_total_rides

    # Returns a dict where the keys are ride names, and the values are total weights (i.e., wait times plus ride times)
    def set_ride_weights(self) -> dict:
        return {self.all_rides[i]: self.wait_times[i] + self.ride_times[i] for i in range(len(self.all_rides))}

    # Maximizes the total number of rides to go on, given user constraints
    def maximize_rides(self, ride_weights: dict) -> list | None:
        prob = pulp.LpProblem("Maximize the number of total rides to go on", pulp.LpMaximize)

        # Variable: ride_i will be an LpInteger with a lower bound of 0 and an upper bound of the maximum number of times a single ride can be rode constraint (set by the user)
        rides = pulp.LpVariable.dicts("ride", ride_weights.keys(), lowBound=0, upBound=self.max_ride_repeats,  cat=pulp.LpInteger)

        # Variable: ride_rode_i will be an LpBinary that is used in the minimum distinct rides constraint (set by the user)
        rides_rode = pulp.LpVariable.dicts("ride_rode",
                                        ride_weights.keys(), cat=pulp.LpBinary)
        
        # Objective function: maximize the sum of ride_i's
        prob += pulp.lpSum(rides[i] for i in ride_weights.keys())

        # Constraint: the sum of the dot product of the rides and their corresponding weights must be at most the user's max time constraint
        #   - In this case, the user must set a max time constraint, or else the solution would be unbounded
        if self.max_time != None:
            prob += pulp.lpDot([rides[i] for i in ride_weights.keys()], [ride_weights.get(i) for i in ride_weights.keys()]) <= self.max_time
        else:
            return None
        
        # Constraint: ride_i >= 1 if the user wants to ride ride_i at least once
        # Constraint: ride_i = 0 if the user wants to avoid ride_i all together
        # User cannot require to go on a ride while also avoiding it
        if self.require_and_avoid:
                return None 
        if self.required_rides != None:
            for i in self.all_rides:
                if i in self.required_rides:
                    prob += rides[i] >= 1
        if self.avoid_rides != None:
            for i in self.all_rides:
                if i in self.avoid_rides:
                    prob += rides[i] == 0

        prob.solve()

        # Check to see if the solution is optimal
        if pulp.LpStatus[prob.status] == "Optimal":
            return ({i: pulp.value(rides[i]) for i in ride_weights.keys()})
        else:
            return None
