import streamlit as st

def guide():
    st.markdown("<h1 style='text-align: center;'>Amusement Park Rides Optimizer</h1", unsafe_allow_html=True)
    st.markdown("This is an interactive web app that uses [integer programming](https://en.wikipedia.org/wiki/Integer_programming) to solve optimization problems involving wait times for amusement park rides.")

    st.markdown("<h3 style='text-align: center;'>Optimization Models</h3", unsafe_allow_html=True)
    st.markdown("This app solves the following optimization problems:")
    with st.expander("Maximize the total number of rides a user goes on within a given time frame"):
        # Informal Description
        with st.expander("Informal Description"):
            st.markdown("This optimization problem seeks to maximize the total number of rides a user goes on, given the following constraints:", help="The user can choose whether or not to allow ride repeats within the optimal solution (reference the constraints below)")
            st.markdown("* The user is willing to spend a combined total of at most $t$ minutes waiting in line to go on all rides within the optimal solution")
            st.markdown("* The user can choose which rides to go on at least once")
            st.markdown("* The user can choose which rides to avoid entirely")
            st.markdown("* The user can choose the minimum number of distinct rides to go on at least once")
            st.markdown("* The user can choose the maximum number of times a ride can be repeated")

        # Formal Description
        with st.expander("Formal Description"):

            # Definition
            st.subheader("Variables:")
            st.markdown("Let R be the set of all unique rides $r_i$")
            st.markdown("Let $r_{(i, o)}$ be the number of times a user goes on ride $r_i$")
            st.markdown("Let $r_{(i, w)}$ be the wait time to go on ride $r_i$")
            st.markdown("Let $w := \sum_{r_i \in R}r_{(i, o)} \cdot r_{(i, w)}$", help="$w$ is the total amount time a user spends waiting in line to go on rides")

            # User-defined Variables
            st.subheader("User-defined Variables:")
            st.markdown("Let $t$ be the maximum cummulative sum a user is willing to spend waiting in line to go on rides", help="This leads to the constraint: $w \leq t$")
            st.markdown("Let $m$ be the maximum number of times a user is willing to repeat going on any given ride $r_i$")
            st.markdown("Let $d$ be the minimum number of distinct rides a user wants to go on at least once")

            # Ternary variable definition
            st.markdown("Let $r_{(i, p)}$ be a ternary variable indicating whether a user wants to go on ride $i$ at least once, or avoid it entirely")
            st.markdown("* $r_{(i, p)} = 0$ implies that the user wants to avoid $r_i$ entirely")
            st.markdown("* $r_{(i, p)} = 1$ implies that the user wants to go on $r_i$ at least once")
            st.markdown("* $r_{(i, p)} = 2$ implies that the user has no preference")

            # Binary variable definition
            st.markdown("Let $r_{(i, u)}$ be a binary variable keeping track of whether a user has gone on ride $r_i$ at least once")
            st.markdown("* $r_{(i, u)}$ = 1 implies that the user has gone on ride $r_i$ at least once")
            st.markdown("* $r_{(i, u)}$ = 0 imples that the user has not gone at ride $r_i$")
            st.subheader("Objective Function:")
            st.latex("\max \sum_{r_i \in R} r_{(i, o)}", help="Maximize the total number of rides a user goes on")

            # Constraints
            st.markdown("Subject to:")
            st.latex("\\forall {r_i \in R}, r_{(i, o)} <= m", help="The user goes any given ride $r_i$ at most m time")
            st.latex("w <= t", help="The total amount of time the user spends waiting in line to go on rides is less than $t$")
            st.latex("r_{(i, p)} = 1 \implies r_{(i, o)} \geq 1", help="If the user wants to go on ride $r_i$ at least once, then $r_{(i, o)} \geq 1$")
            st.latex("r_{(i, p)} = 0 \implies r_{(i, o)} = 0", help="If the user wants to avoid going on ride $r_i$ entirely, then $r_{(i, o)} = 0")
            st.latex("r_{(i, o)} \geq r_{(i, u)}", help="Enforces the binary decision variable $r_{(i, u)}$")
            st.latex("\sum_{r_i \in R} r_{(i, u)} \geq d", help="Enforces the minimum number of distinct rides constraint")
            st.latex("r_{(i, o)}, r_{(i, w)}, t, d, m \in \mathbb{N}^+")
            st.latex("r_{(i, u)} \in \{0, 1\}")
            st.latex("r_{(i, p)} \in \{0, 1, 2\}")

        # Optimal solution
        st.markdown("The optimal solution (found in the **Results** section below) determines which rides the user should go on (and how many times).")

    with st.expander("Minimize the total amount of time a user spends waiting in line to go on rides"):
        # Informal Description
        with st.expander("Informal Description"):
            st.markdown("This optimization problem seeks to minimize the total amount of time a user spends waiting in line to go on rides, given the following constraints:", help="The user can choose whether or not to allow ride repeats within the optimal solution (reference the constraints below)")
            st.markdown("* The user wants to go on at least $n$ total rides", help="The user can choose whether or not $n$ includes ride repeats")
            st.markdown("* The user can choose which rides to go on at least once")
            st.markdown("* The user can choose which rides to avoid entirely")
            st.markdown("* The user can choose the minimum number of distinct rides to go on at least once")
            st.markdown("* The user can choose the maximum number of times a ride can be repeated")

        # Formal Description
        with st.expander("Formal description of minimization problem"):

            # Definitions
            st.subheader("Variables:")
            st.markdown("Let R be the set of all unique rides $r_i$")
            st.markdown("Let $r_{(i, o)}$ be the number of times a user goes on ride $r_i$")
            st.markdown("Let $r_{(i, w)}$ be the wait time to go on ride $r_i$")

            #User-defined Variables
            st.subheader("User-defined Variables:")
            st.markdown("Let $d$ be the minimum number of distinct rides a user wants to go on at least once")
            st.markdown("Let $m$ be the maximum number of times a user is willing to repeat going on a ride")
            st.markdown("Let $t$ be the minimum number of total rides a user wants to go on", help="This includes ride repeats if $m \geq 2$")

            # Ternary variable definition
            st.markdown("Let $r_{(i, p)}$ be a ternary variable indicating whether a user wants to go on ride $i$ at least once, or avoid it entirely")
            st.markdown("* $r_{(i, p)} = 0$ implies that the user wants to avoid $r_i$ entirely")
            st.markdown("* $r_{(i, p)} = 1$ implies that the user wants to go on $r_i$ at least once")
            st.markdown("* $r_{(i, p)} = 2$ implies that the user has no preference")

            # Binary variable definition
            st.markdown("Let $r_{(i, u)}$ be a binary variable keeping track of whether a user has gone on ride $r_i$ at least once")
            st.markdown("* $r_{(i, u)}$ = 1 implies that the user has gone on ride $r_i$ at least once")
            st.markdown("* $r_{(i, u)}$ = 0 imples that the user has not gone at ride $r_i$")

            # Objective Function
            st.subheader("Objective Function:")
            st.latex("\min \sum_{r_i \in R} r_{(i, w)}", help="Minimize the cummulative sum of minutes a user spends waiting in line to go on rides")

            # Constraints
            st.markdown("Subject to:")
            st.latex("\sum_{r_i \in R} r_{(i, o)} \geq t", help="The total number of rides the user goes on is at least $t$")
            st.latex("\\forall {r_i \in R}, r_{(i, o)} <= m", help="The user goes any given ride $r_i$ at most m times")
            st.latex("r_{(i, p)} = 1 \implies r_{(i, o)} \geq 1", help="If the user wants to go on ride $r_i$ at least once, then $r_{(i, o)} \geq 1$")
            st.latex("r_{(i, p)} = 0 \implies r_{(i, o)} = 0", help="If the user wants to avoid going on ride $r_i$ entirely, then $r_{(i, o)} = 0")
            st.latex("r_{(i, o)} \geq r_{(i, u)}", help="Enforces the binary decision variable $r_{(i, u)}$")
            st.latex("\sum_{r_i \in R} r_{(i, u)} \geq d", help="Enforces the minimum number of distinct rides constraint")
            st.latex("r_{(i, o)}, r_{(i, w)}, d, m, t \in \mathbb{N^+}")
            st.latex("r_{(i, u)} \in \{0, 1\}")
            st.latex("r_{(i, p)} \in \{0, 1, 2\}")

        # Optimal solution
        st.markdown("The optimal solution (found in the **Results** section below) determines which rides the user should go on (and how many times).")



    # Model Assumptions
    st.markdown("<h3 style='text-align: center;'>Model Assumptions</h3", unsafe_allow_html=True)
    st.markdown("The optimization models within this app assume that all ride wait times are constant and do not change.")

    # Park Data
    st.markdown("<h3 style='text-align: center;'>Park Data</h3", unsafe_allow_html=True)
    st.markdown("This app features a **Demo** mode where randomly-generated data is used as input for the optimization models.")
    st.markdown("This app also includes real-time ride wait times for the following California amusement parks:", help="Use the **Park** dropdown in the sidebar menu to select which data the optimization models will use")
    st.markdown("* **Disneyland Resort Magic Kingdom**")
    st.markdown("* **Disneyland Resort California Adventure**")
    st.markdown("* **Universal Studios**")
    st.markdown(">The California amusement park data is from: (https://themeparks.wiki/)")
    st.divider()
