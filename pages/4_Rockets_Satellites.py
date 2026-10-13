import streamlit as st
import pandas as pd
from db import run_query, execute_query

# --- AUTHENTICATION CHECK ---
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in from the Home Dashboard first.")
    st.stop()

st.title("🛰️ Rockets & Satellites")
st.sidebar.markdown(f"**👤 User:** {st.session_state.username}")
st.sidebar.markdown(f"**🛡️ Role:** {st.session_state.role}")

tab_view, tab_rocket, tab_satellite = st.tabs(["View Hardware", "Add Rocket", "Add Satellite"])

# 1. VIEW HARDWARE
with tab_view:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Rockets Directory")
        rocket_query = """
            SELECT r.rocket_name, a.agency_name, r.payload_capacity_kg, r.cost_million 
            FROM Rockets r
            LEFT JOIN Agencies a ON r.agency_id = a.agency_id
        """
        st.dataframe(run_query(rocket_query), use_container_width=True)
        
    with col2:
        st.subheader("Satellites & Payloads")
        sat_query = """
            SELECT s.satellite_name, m.mission_name, s.orbit_type, s.weight_kg 
            FROM Satellites s
            LEFT JOIN Missions m ON s.mission_id = m.mission_id
        """
        st.dataframe(run_query(sat_query), use_container_width=True)

# 2. ADD ROCKET
with tab_rocket:
    st.subheader("Register New Rocket")
    if st.session_state.role == 'admin_user':
        with st.form("add_rocket_form"):
            r_name = st.text_input("Rocket Name")
            
            agencies = run_query("SELECT agency_id, agency_name FROM Agencies")
            agency = st.selectbox("Operating Agency", agencies['agency_name'].tolist())
            
            payload = st.number_input("Payload Capacity (kg)", min_value=0.0, format="%.2f")
            cost = st.number_input("Cost (Millions $)", min_value=0.0, format="%.2f")
            
            submitted = st.form_submit_button("Add Rocket")
            if submitted:
                ag_id = agencies.loc[agencies['agency_name'] == agency, 'agency_id'].values[0]
                insert_q = "INSERT INTO Rockets (rocket_name, agency_id, payload_capacity_kg, cost_million) VALUES (%s, %s, %s, %s)"
                try:
                    execute_query(insert_q, (r_name, int(ag_id), float(payload), float(cost)))
                    st.success("Rocket added successfully! ✅")
                except Exception as e:
                    st.error(f"Error: {e} ❌")
    else:
        st.error("Permission Denied: Only Admins can add rockets. ❌")

# 3. ADD SATELLITE
with tab_satellite:
    st.subheader("Register New Satellite")
    if st.session_state.role == 'admin_user':
        missions = run_query("SELECT mission_id, mission_name FROM Missions")
        
        if not missions.empty:
            with st.form("add_satellite_form"):
                s_name = st.text_input("Satellite Name")
                sel_mission = st.selectbox("Associated Mission", missions['mission_name'].tolist())
                orbit = st.text_input("Orbit Type (e.g., LEO, GEO, Lunar)")
                weight = st.number_input("Weight (kg)", min_value=0.0, format="%.2f")
                
                submitted = st.form_submit_button("Add Satellite")
                if submitted:
                    m_id = missions.loc[missions['mission_name'] == sel_mission, 'mission_id'].values[0]
                    insert_q = "INSERT INTO Satellites (satellite_name, mission_id, orbit_type, weight_kg) VALUES (%s, %s, %s, %s)"
                    try:
                        execute_query(insert_q, (s_name, int(m_id), orbit, float(weight)))
                        st.success("Satellite added successfully! ✅")
                    except Exception as e:
                        st.error(f"Error: {e} ❌")
        else:
            st.info("Ensure at least one Mission exists before adding satellites.")
    else:
        st.error("Permission Denied: Only Admins can add satellites. ❌")