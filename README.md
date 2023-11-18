# Table of Contents
- [Table of Contents](#table-of-contents)
- [Project Description](#project-description)
- [Features](#features)
- [Credits](#credits)

# Project Description
This is an interactive web app that uses [integer programming](https://en.wikipedia.org/wiki/Integer_programming) to optimize your ride selection at various amusement parks based on ride wait times and personal constraints/preferences.
* A formal description of the optimization problems solved be be found on the app: https://rides-optimizer.streamlit.app/ 

# Features
- [x] Multiple optimization models to cover various assumptions regarding the amount of time it takes waiting in line for a given ride
- [x] Optimization models can be applied to real-time data from 3 major California amusement parks
  * Disneyland Resort Magic Kingdom
  * Disneyland Resort California Adventure
  * Universal Studios
- [x] Optimization models can also be applied in a demo mode for testing things out
- [x] Support for user preferences such as:
  * Which rides the user wants to go on at least once
  * Which rides the user wants to avoid all together
  * Maximum number of times a user wants to go on a given ride
  * Minimum number of distinct rides a user wants to go on

# Credits
This app uses [ThemeParks API](https://themeparks.wiki/) to gather real-time data of ride wait times from various amusement parks.