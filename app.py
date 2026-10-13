import streamlit as st
import pandas as pd
import plotly.express as px
from db import run_query

# Page config must be the first Streamlit command
st.set_page_config(page_title="Space Mission Tracker", layout="wide")

# --- CUSTOM CSS FOR GRADIENT TITLE ---
st.markdown("""
    <style>
    .gradient-text {
        background: linear-gradient(to right, #00FFFF, #800080);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = None
if 'username' not in st.session_state:
    st.session_state.username = None

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.markdown('<p class="gradient-text">Space Mission Tracker 🚀</p>', unsafe_allow_html=True)
    st.subheader("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # Check against Users table
        query = "SELECT role FROM Users WHERE username = %s AND password = %s"
        result = run_query(query, (username, password))
        
        if not result.empty:
            st.session_state.logged_in = True
            st.session_state.role = result.iloc[0]['role']
            st.session_state.username = username
            st.success(f"Welcome {username}! Logged in as {st.session_state.role}.")
            st.rerun()
        else:
            st.error("Invalid username or password.")

# --- MAIN DASHBOARD ---
else:
    st.sidebar.markdown(f"**👤 User:** {st.session_state.username}")
    st.sidebar.markdown(f"**🛡️ Role:** {st.session_state.role}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.rerun()

    st.markdown('<p class="gradient-text">Home Dashboard 🛰️</p>', unsafe_allow_html=True)

    # 1. Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    
    missions_count = run_query("SELECT COUNT(*) as count FROM Missions").iloc[0]['count']
    launches_count = run_query("SELECT COUNT(*) as count FROM Launches").iloc[0]['count']
    astronauts_count = run_query("SELECT COUNT(*) as count FROM Astronauts").iloc[0]['count']
    satellites_count = run_query("SELECT COUNT(*) as count FROM Satellites").iloc[0]['count']

    with col1:
        st.metric("Total Missions", missions_count)
    with col2:
        st.metric("Total Launches", launches_count)
    with col3:
        st.metric("Astronauts", astronauts_count)
    with col4:
        st.metric("Satellites", satellites_count)

    st.markdown("---")

    # 2. Charts
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Missions per Agency")
        agency_df = run_query("""
            SELECT a.agency_name, COUNT(m.mission_id) as mission_count 
            FROM Missions m 
            JOIN Agencies a ON m.agency_id = a.agency_id 
            GROUP BY a.agency_name
        """)
        if not agency_df.empty:
            fig1 = px.bar(agency_df, x='agency_name', y='mission_count', 
                          color_discrete_sequence=['#00FFFF'])
            st.plotly_chart(fig1, use_container_width=True)

    with chart_col2:
        st.subheader("Mission Status Distribution")
        status_df = run_query("""
            SELECT status, COUNT(*) as count 
            FROM Missions 
            GROUP BY status
        """)
        if not status_df.empty:
            fig2 = px.pie(status_df, names='status', values='count', 
                          color_discrete_sequence=px.colors.sequential.Purp)
            st.plotly_chart(fig2, use_container_width=True)