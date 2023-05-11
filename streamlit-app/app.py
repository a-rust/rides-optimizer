import streamlit as st
import demo_constant
import demo_dynamic
import park_data


def define_park():
    park = st.sidebar.selectbox(label="Park", options=("Demo", "Disneyland Resort Magic Kingdom", "Disneyland Resort California Adventure", "Universal Studios"))
    if park == "Demo":
        st.markdown("<h1 style='text-align: center;'>Demo</h1", unsafe_allow_html=True)
    elif park == "Disneyland Resort Magic Kingdom":
        st.markdown("<h1 style='text-align: center;'>Disneyland Resort Magic Kingdom</h1", unsafe_allow_html=True)
    elif park == "Disneyland Resort California Adventure":
        st.markdown("<h1 style='text-align: center;'>Disneyland Resort California Adventure</h1")
    elif park == "Universal Studios":
        st.markdown("<h1 style='text-align: center;'>Universal Studios</h1", unsafe_allow_html=True)
    return park

def define_time_assumption():
    time_assumption = st.selectbox("Please select the time assumptions to be used", ("Constant", "Dynamic"), help="Do you want to assume constant or dynamic wait and ride times?")
    return time_assumption

def main():
    park = define_park()
    time_assumption = define_time_assumption()
    if park == "Demo":
        if time_assumption == "Constant":
            demo_constant.main()
        elif time_assumption == "Dynamic":
            demo_dynamic.main()

main()
