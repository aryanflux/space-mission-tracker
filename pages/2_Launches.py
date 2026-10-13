import streamlit as st
import pandas as pd
from db import run_query, execute_query

# --- AUTHENTICATION CHECK ---
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in from the Home Dashboard first.")
    st.stop()

st.title("🚀 Launch Schedule & Records")
st.sidebar.markdown(f"**👤 User:** {st.session_state.username}")
st.sidebar.markdown(f"**🛡️ Role:** {st.session_state.role}")

tab_view, tab_schedule, tab_update = st.tabs(["View Launches", "Schedule a Launch", "Record Outcome"])

# 1. VIEW LAUNCHES
with tab_view:
    st.subheader("Launch History & Schedule")
    query = """
        SELECT l.launch_id, m.mission_name, r.rocket_name, s.site_name, l.launch_date, l.outcome 
        FROM Launches l
        LEFT JOIN Missions m ON l.mission_id = m.mission_id
        LEFT JOIN Rockets r ON l.rocket_id = r.rocket_id
        LEFT JOIN Launch_Sites s ON l.site_id = s.site_id
        ORDER BY l.launch_date DESC
    """
    df = run_query(query)
    st.dataframe(df, use_container_width=True)

# 2. SCHEDULE A LAUNCH
with tab_schedule:
    st.subheader("Schedule a New Launch")
    if st.session_state.role in ['admin_user', 'control_user']:
        with st.form("schedule_launch_form"):
            # Fetch data for dropdowns
            missions = run_query("SELECT mission_id, mission_name FROM Missions")
            rockets = run_query("SELECT rocket_id, rocket_name FROM Rockets")
            sites = run_query("SELECT site_id, site_name FROM Launch_Sites")
            
            sel_mission = st.selectbox("Mission", missions['mission_name'].tolist())
            sel_rocket = st.selectbox("Rocket", rockets['rocket_name'].tolist())
            sel_site = st.selectbox("Launch Site", sites['site_name'].tolist())
            
            launch_date = st.date_input("Launch Date")
            outcome = st.selectbox("Initial Outcome / Status", ["Scheduled", "Success", "Failed", "Delayed"])
            
            submitted = st.form_submit_button("Schedule Launch")
            if submitted:
                m_id = missions.loc[missions['mission_name'] == sel_mission, 'mission_id'].values[0]
                r_id = rockets.loc[rockets['rocket_name'] == sel_rocket, 'rocket_id'].values[0]
                s_id = sites.loc[sites['site_name'] == sel_site, 'site_id'].values[0]
                
                insert_q = """INSERT INTO Launches (mission_id, rocket_id, site_id, launch_date, outcome) 
                              VALUES (%s, %s, %s, %s, %s)"""
                try:
                    execute_query(insert_q, (int(m_id), int(r_id), int(s_id), launch_date, outcome))
                    st.success("Launch scheduled successfully! ✅")
                except Exception as e:
                    st.error(f"Error: {e} ❌")
    else:
        st.error("Permission Denied: Public users cannot schedule launches. ❌")

# 3. RECORD / UPDATE OUTCOME
with tab_update:
    st.subheader("Update Launch Outcome")
    if st.session_state.role in ['admin_user', 'control_user']:
        launches = run_query("""
            SELECT l.launch_id, CONCAT(m.mission_name, ' (', l.launch_date, ')') as launch_desc 
            FROM Launches l
            JOIN Missions m ON l.mission_id = m.mission_id
        """)
        
        if not launches.empty:
            with st.form("update_outcome_form"):
                target_launch = st.selectbox("Select Launch", launches['launch_desc'].tolist())
                new_outcome = st.selectbox("Update Outcome", ["Success", "Failed", "Delayed", "Scheduled"])
                
                updated = st.form_submit_button("Record Outcome")
                if updated:
                    l_id = launches.loc[launches['launch_desc'] == target_launch, 'launch_id'].values[0]
                    update_q = "UPDATE Launches SET outcome = %s WHERE launch_id = %s"
                    try:
                        execute_query(update_q, (new_outcome, int(l_id)))
                        st.success("Launch outcome updated successfully! ✅")
                    except Exception as e:
                        st.error(f"Error: {e} ❌")
        else:
            st.info("No launches available to update.")
    else:
        st.error("Permission Denied: Public users cannot update launch outcomes. ❌")