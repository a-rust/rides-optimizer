# Table of Contents
- [Table of Contents](#table-of-contents)
- [Project Description](#project-description)
- [Optimization Problems Solved](#optimization-problems-solved)
  - [Constraints](#constraints)
  - [Assumptions](#assumptions)
  - [Limitations](#limitations)
  - [Future Considerations](#future-considerations)
- [Credits](#credits)

# Project Description
An interactive web app that solves various optimization problems involving amusement park rides and their wait times.

# Optimization Problems Solved
Given a set of amusement park rides (and their wait times),
1. Maximize the total number of rides to go on.
2. Minimize the total amount of time spent waiting in line for rides.

## Constraints
To make something meaningful out of these optimization problems, there need to be some constraints - both required and optional:
* **Required Constraints**
  * Maximum total amount of time allowed waiting in line for rides
    * Only applies to the maximization problem above
  * Minimum number of total rides to go on
    * Only applies to the minimization problem above
* **Optional Constraints**
  * Which rides does the user want to go on at least once?
  * Which rides does the user want to avoid all together?
  * What is the minimum number of distinct rides that the user wants to go on at least once?
  * What is the maximum number of times the user wants to ride any given ride?

## Assumptions
This app offers 2 distinct models, each under a different time assumption regarding the wait times of park rides:
1. Constant wait times
2. Dynamically changing wait times

The wait time assumption influences the formalization of each optimization problem

## Limitations
* These optimization problems only solve for the optimal **set** of rides to go on, not the **path itself**
  * For example, if the optimal solution includes rides $\{r_1, r_2, r_3\}$, this app will not solve for an optimal path including these vertices.
    * One attempt to solve this would be to consider the distances between rides, and reconstruct the optimization problems using graphs with weighted edges
* The optimization model with dynamically changing wait times is really only practical if the wait times at each time period are known beforehand


## Future Considerations
There are many different ways to build off of this project. Some considerations are:
* Solve for the optimal path instead of the optimal set of rides
* Build a predictive model to deal with the limitations of the dynamically changing wait times assumptions
* Add features to deal with uncertainty such as weather, congestion, etc.

# Credits
This app uses [ThemeParks API](https://themeparks.wiki/) to gather real-time data regarding the wait times of rides at major amusement parks all around the world. 
