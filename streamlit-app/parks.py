import streamlit as st
import pandas as pd
import random
import sys
import os
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path)
import park_data


class OptimizePark():
    def __init__(self, name: str, all_rides: dict, active_rides: dict, time_assumption: str, optimization_problem: str) -> None:
        self.name = name
        self.all_rides = all_rides
        self.active_rides = active_rides
        self.time_assumption = time_assumption
        self.optimization_problem = optimization_problem
