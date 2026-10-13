import streamlit as st
import pandas as pd
import plotly.express as px
from db import run_query

# --- AUTHENTICATION CHECK ---
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in from the Home Dashboard first.")
    st.stop()

st.title("📊 Advanced Reports & Analytics")
st.sidebar.markdown(f"**👤 User:** {st.session_state.username}")
st.sidebar.markdown(f"**🛡️ Role:** {st.session_state.role}")

# 1. GROUP BY and HAVING 
st.subheader("Agency Mission Breakdown (GROUP BY & HAVING)")
query_group = """
    SELECT a.agency_name, COUNT(m.mission_id) AS total_missions, SUM(m.budget_million) AS total_budget
    FROM Agencies a
    JOIN Missions m ON a.agency_id = m.agency_id
    GROUP BY a.agency_name
    HAVING total_missions >= 1
"""
df_group = run_query(query_group)

col1, col2 = st.columns(2)
with col1:
    st.write("Data Table:")
    st.dataframe(df_group, use_container_width=True)

with col2:
    if not df_group.empty:
        # Utilizing cyan and purple theme accents
        fig1 = px.bar(df_group, x='agency_name', y='total_missions', 
                      color='total_budget',
                      color_continuous_scale=['#00FFFF', '#800080'],
                      title="Missions & Budgets per Agency")
        st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# 2. Complex JOINs
st.subheader("Comprehensive Launch History (INNER & LEFT JOINs)")
query_join = """
    SELECT m.mission_name, r.rocket_name, s.site_name, l.launch_date, l.outcome
    FROM Launches l
    INNER JOIN Missions m ON l.mission_id = m.mission_id
    LEFT JOIN Rockets r ON l.rocket_id = r.rocket_id
    LEFT JOIN Launch_Sites s ON l.site_id = s.site_id
    ORDER BY l.launch_date DESC
"""
df_join = run_query(query_join)

# Data Table
st.dataframe(df_join, use_container_width=True)

# Chart
if not df_join.empty:
    fig2 = px.histogram(df_join, x='outcome', color='rocket_name',
                        color_discrete_sequence=px.colors.qualitative.Pastel,
                        title="Launch Outcomes Breakdown by Rocket")
    st.plotly_chart(fig2, use_container_width=True)