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

# Maximizes the total number of rides to go on over all time steps
    def maximize_rides(self, ride_weights: dict) -> list | None:

        prob = pulp.LpProblem("Maximize the number of total rides to go on over dynamically changing time steps", pulp.LpMaximize)

        # Variable: ride_time_step_(i, j) will represent the number of times ride i is rode during time period j
        rides = pulp.LpVariable.dicts("ride_time_step", [(ride, time_period) for ride in ride_weights.keys() for  time_period in range(1, self.time_steps+1)], lowBound=0, upBound=self.max_ride_repeats,  cat=pulp.LpInteger)

        # Objective function: maximize the sum of ride_i's 
        prob += pulp.lpSum(rides[(ride, time_period)] for ride in ride_weights.keys() for time_period in range(1, self.time_steps+1))

        # Constraint: the sum of the dot product of the rides and their corresponding weights in each time step must be at most the user's max time constraint
        if self.max_time != None:
            for time_step in range(1, self.time_steps+1):
                prob += pulp.lpDot(list(ride_weights[ride][time_step-1] for ride in ride_weights.keys()), [rides[(ride, time_step)] for ride in ride_weights.keys()]) <= self.max_time[time_step-1]

        # Constraint: ride_(i, j) >= 1 for at least one time step j if the user wants to ride ride_i at least once
        # Constraint: ride_(i, j) = 0 for all time steps j if the user wants to avoid ride_i all together
        # User cannot require to go on a ride while also avoiding it
        if self.require_and_avoid:
                return None 
        if self.required_rides != None:
            for i in self.all_rides:
                if i in self.required_rides:
                    # If the sum of rides[i, j] >= 1 for all time steps j, then the required constraint was satisfied
                    prob += pulp.lpSum(rides[i, j] for j in range(1, self.time_steps+1)) >= 1
        if self.avoid_rides != None:
            for i in self.all_rides:
                if i in self.avoid_rides:
                    # If the sum of rides[i, j] = 0 for all time steps j, then the avoid constraint was satisfied
                    prob += pulp.lpSum(rides[i, j] for j in range(1, self.time_steps+1)) == 0

        # Constraint: The sum of a ride over all time steps must be less than the max ride repeats preference set by the user
        for i in ride_weights.keys():
            prob += pulp.lpSum(rides[i, time_step] for time_step in range(1, self.time_steps+1)) <= self.max_ride_repeats

        prob.solve()

        if pulp.LpStatus[prob.status] == "Optimal":
            return ({(ride, time_step): pulp.value(rides[ride, time_step]) for ride in ride_weights.keys() for time_step in range(1, self.time_steps+1)})
        else:
            return None        
