import requests
import streamlit as st

class ParkData:
    def __init__(self, url: str) -> None:
        self.url = url
        self.rides = {}
        self.active_rides = {}

    # Caching the data for 3600 seconds to avoid spamming api requests
    @st.cache_data(ttl=3600)
    def api_request(_self):
        url_request = requests.get(_self.url)
        return url_request.json()

    def get_all_rides(self):
        data = self.api_request()
        for item in data:
            self.rides.update({item["name"]: item["waitTime"]})
        return self.rides

    # Function to filter for currently active rides only (i.e., rides with a waitTime not equal to None)
    def filter_for_active_rides(self):
        data = self.api_request()
        for item in data:
            if item["active"] != False:
                self.active_rides.update({item["name"]: item["waitTime"]})
        return self.active_rides


# Check out https://www.themeparks.wiki/ for the park data and API documentation
disney_kingdom = ParkData("https://api.themeparks.wiki/preview/parks/DisneylandResortMagicKingdom/waittime")
california_adventure = ParkData("https://api.themeparks.wiki/preview/parks/DisneylandResortCaliforniaAdventure/waittime")
universal_studios = ParkData("https://api.themeparks.wiki/preview/parks/UniversalStudios/waittime")