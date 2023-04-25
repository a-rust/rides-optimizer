# Table of Contents
- [Table of Contents](#table-of-contents)
- [Project Description](#project-description)
- [Optimization Problems Solved](#optimization-problems-solved)
  - [Constraints](#constraints)
  - [Assumptions](#assumptions)
  - [Approaches](#approaches)
  - [Limitations](#limitations)
  - [Web App](#web-app)

# Project Description
An interactive web app to demonstrate optimal solutions to various optimization problems involving amusement park rides.

# Optimization Problems Solved
Given an amusement park with a set of rides (and their wait and ride times),
1. Maximize the number of rides to go on.
2. Minimize the amount of time spent in the park.

## Constraints
To make something meaningful out of these optimization problems, there need to be some constraints - ideally a set of preferences from a user that will actually go to the park later on. These may include:
* **Ride preferences**
  * Which rides does the user want to go on at least once?
  * Which rides does the user want to avoid all together?
* **Maximum total time allowed at the park**
  * This only accounts for the total time waiting in line for rides + actually riding them
    * More on this in the [here](#limitations)
  * Only applies to the maximization problem above
* **Minimum number of total rides to go on**
  * Only applies to the minimization problem above
* **Minimum number of distinct rides to go on at least once**
  * Can apply to both problems
* **Maximum number of times a ride can be repeated**
  * Can apply to both problems

## Assumptions
There are some assumptions that must be considered. These include
* Can either assume constant, or dynamically changing wait and ride times
  * Dynamically changing wait times are probably more realistic
    * Wait times are dependent on congestion, which dynamically changes at an amusement park
  * There could be an argument for both constant and dynamically changing ride times
    * The ride times themselves do not really change due to congestion, aside from maybe some small epsilon due to congestion

## Approaches
* For the constant time assumptions, mixed integer programming can be used

## Limitations
* These optimization problems only solve for the optimal set of rides to go on, not the path itself of rides to go on
  * For example, if the optimal solution includes rides $\{r_1, r_2, r_3\}$, there will be no optimal path including which ride to ride first, second, etc.
    * One attempt to solve this would be to consider the distances between rides, and reconstruct the optimization problems using graphs with weighted edges

## Web App
TODO
