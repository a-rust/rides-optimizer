import streamlit as st
import requests

import demo_constant
import demo_dynamic
import park_data
import parks
import instructions

# Caching the data for 3600 seconds to avoid spamming api requests
@st.cache_data(ttl=3600)
def api_request(url):
    url_request = requests.get(url)
    return url_request.json()

def define_park():
    park = st.sidebar.selectbox(label="Park", options=("Demo", "Disneyland Resort Magic Kingdom", "Disneyland Resort California Adventure", "Universal Studios"))
    if park == "Demo":
        st.markdown("<h1 style='text-align: center;'>Demo</h1", unsafe_allow_html=True)
    elif park == "Disneyland Resort Magic Kingdom":
        st.markdown("<h1 style='text-align: center;'>Disneyland Resort Magic Kingdom</h1", unsafe_allow_html=True)
    elif park == "Disneyland Resort California Adventure":
        st.markdown("<h1 style='text-align: center;'>Disneyland Resort California Adventure</h1", unsafe_allow_html=True)
    elif park == "Universal Studios":
        st.markdown("<h1 style='text-align: center;'>Universal Studios</h1", unsafe_allow_html=True)
    return park

def define_time_assumption():
    time_assumption = st.selectbox("Please select the time assumptions to be used", ("Constant", "Dynamic"), help="Do you want to assume constant or dynamic wait and ride times?")
    return time_assumption

def main():
    instructions.guide()
    park = define_park()
    time_assumption = define_time_assumption()
    if park == "Demo":
        if time_assumption == "Constant":
            demo_constant.main()
        elif time_assumption == "Dynamic":
            demo_dynamic.main()
    elif park == "Disneyland Resort Magic Kingdom":
        rides = api_request("https://api.themeparks.wiki/preview/parks/DisneylandResortMagicKingdom/waittime")
        disney_kingdom = park_data.ParkData(rides)
        p = parks.OptimizePark(park, disney_kingdom.filter_for_active_rides(), time_assumption)
        p.main()
    elif park == "Disneyland Resort California Adventure":
        rides = api_request("https://api.themeparks.wiki/preview/parks/DisneylandResortCaliforniaAdventure/waittime")
        california_adventure = park_data.ParkData(rides)
        p = parks.OptimizePark(park, california_adventure.filter_for_active_rides(), time_assumption)
        p.main()
    
    elif park == "Universal Studios":
        rides = api_request("https://api.themeparks.wiki/preview/parks/UniversalStudios/waittime")
        universal_studios = park_data.ParkData(rides)
        p = parks.OptimizePark(park, universal_studios.filter_for_active_rides(), time_assumption)
        p.main()
        
main()
