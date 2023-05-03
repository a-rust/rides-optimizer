import streamlit as st
import demo_constant
import demo_dynamic

def define_problem():
    park = st.sidebar.selectbox(label="Park", options=("Demo", "Empty for now"))
    if park == "Demo":
        st.markdown("<h1 style='text-align: center;'>Demo</h1", unsafe_allow_html=True)
        time_assumption = st.selectbox("Please select the time assumptions to be used", ("Constant", "Dynamic"), help="Do you want to assume constant or dynamic wait and ride times?")
        return time_assumption
    else:
        return

def main():
    time_assumption = define_problem()
    if time_assumption == "Constant":
        demo_constant.main()
    else:
        demo_dynamic.main()

main()
