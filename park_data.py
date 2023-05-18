import requests
import streamlit as st

class ParkData:
    def __init__(self, cached_data: list) -> None:
        self.cached_data = cached_data
        self.rides = {}
        self.active_rides = {}

    # Function to filter for currently active rides only (i.e., rides with a waitTime not equal to None)
    def filter_for_active_rides(self):
        for item in self.cached_data:
            if item["active"] != False:
                if item["waitTime"] != None:
                    self.active_rides.update({item["name"]: item["waitTime"]})
                else:
                    self.active_rides.update({item["name"]: 0})
        return self.active_rides

# Check out https://www.themeparks.wiki/ for the park data and API documentation
