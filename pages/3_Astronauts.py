import streamlit as st
import pandas as pd
from db import run_query, execute_query

# --- AUTHENTICATION CHECK ---
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in from the Home Dashboard first.")
    st.stop()

st.title("🧑‍🚀 Astronauts & Crew Roster")
st.sidebar.markdown(f"**👤 User:** {st.session_state.username}")
st.sidebar.markdown(f"**🛡️ Role:** {st.session_state.role}")

tab_view, tab_add, tab_assign = st.tabs(["View Roster", "Add Astronaut", "Assign to Mission"])

# 1. VIEW ROSTER & ASSIGNMENTS
with tab_view:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Astronaut Directory")
        astro_query = """
            SELECT ast.name, ast.nationality, ast.dob, ag.agency_name 
            FROM Astronauts ast
            LEFT JOIN Agencies ag ON ast.agency_id = ag.agency_id
        """
        st.dataframe(run_query(astro_query), use_container_width=True)
        
    with col2:
        st.subheader("Crew Assignments")
        crew_query = """
            SELECT m.mission_name, ast.name as astronaut_name, c.crew_role
            FROM Crew_Assignments c
            JOIN Missions m ON c.mission_id = m.mission_id
            JOIN Astronauts ast ON c.astronaut_id = ast.astronaut_id
        """
        st.dataframe(run_query(crew_query), use_container_width=True)

# 2. ADD ASTRONAUT
with tab_add:
    st.subheader("Register New Astronaut")
    if st.session_state.role == 'admin_user':
        with st.form("add_astronaut_form"):
            name = st.text_input("Full Name")
            nationality = st.text_input("Nationality")
            dob = st.date_input("Date of Birth")
            
            agencies = run_query("SELECT agency_id, agency_name FROM Agencies")
            agency = st.selectbox("Affiliated Agency", agencies['agency_name'].tolist())
            
            submitted = st.form_submit_button("Add Astronaut")
            if submitted:
                ag_id = agencies.loc[agencies['agency_name'] == agency, 'agency_id'].values[0]
                insert_q = "INSERT INTO Astronauts (name, nationality, dob, agency_id) VALUES (%s, %s, %s, %s)"
                try:
                    execute_query(insert_q, (name, nationality, dob, int(ag_id)))
                    st.success("Astronaut added successfully! ✅")
                except Exception as e:
                    st.error(f"Error: {e} ❌")
    else:
        st.error("Permission Denied: Only Admins can add astronauts. ❌")

# 3. ASSIGN TO MISSION (M:N Relationship Resolution)
with tab_assign:
    st.subheader("Assign Crew to Mission")
    if st.session_state.role == 'admin_user':
        missions = run_query("SELECT mission_id, mission_name FROM Missions")
        astronauts = run_query("SELECT astronaut_id, name FROM Astronauts")
        
        if not missions.empty and not astronauts.empty:
            with st.form("assign_crew_form"):
                sel_mission = st.selectbox("Mission", missions['mission_name'].tolist())
                sel_astronaut = st.selectbox("Astronaut", astronauts['name'].tolist())
                role = st.text_input("Crew Role (e.g., Commander, Pilot, Mission Specialist)")
                
                assigned = st.form_submit_button("Assign Astronaut")
                if assigned:
                    m_id = missions.loc[missions['mission_name'] == sel_mission, 'mission_id'].values[0]
                    ast_id = astronauts.loc[astronauts['name'] == sel_astronaut, 'astronaut_id'].values[0]
                    
                    assign_q = "INSERT INTO Crew_Assignments (mission_id, astronaut_id, crew_role) VALUES (%s, %s, %s)"
                    try:
                        execute_query(assign_q, (int(m_id), int(ast_id), role))
                        st.success("Crew assigned successfully! ✅")
                    except Exception as e:
                        st.error(f"Error: {e} ❌")
        else:
            st.info("Ensure both Missions and Astronauts exist before assigning.")
    else:
        st.error("Permission Denied: Only Admins can assign crew. ❌")