import requests
import streamlit as st

class ParkData:
    def __init__(self, cached_data: list) -> None:
        self.cached_data = cached_data
        self.rides = {}
        self.active_rides = {}

    def get_all_rides(self):
        for item in self.cached_data:
            self.rides.update({item["name"]: item["waitTime"]})
        return self.rides

    # Function to filter for currently active rides only (i.e., rides with a waitTime not equal to None)
    def filter_for_active_rides(self):
        for item in self.cached_data:
            if item["active"] != False:
                self.active_rides.update({item["name"]: item["waitTime"]})
        return self.active_rides

# Check out https://www.themeparks.wiki/ for the park data and API documentation
