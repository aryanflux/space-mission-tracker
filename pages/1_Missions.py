import streamlit as st
import pandas as pd
from db import run_query, execute_query

# --- AUTHENTICATION CHECK ---
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in from the Home Dashboard first.")
    st.stop()

st.title("🛰️ Missions Management")
st.sidebar.markdown(f"**👤 User:** {st.session_state.username}")
st.sidebar.markdown(f"**🛡️ Role:** {st.session_state.role}")

# --- TABS FOR CRUD OPERATIONS ---
tab_view, tab_add, tab_update, tab_delete = st.tabs(["View Missions", "Add Mission", "Update Mission", "Delete Mission"])

# 1. VIEW TAB
with tab_view:
    st.subheader("Browse & Search Missions")
    
    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input("Search by Mission Name:")
    with col2:
        status_filter = st.selectbox("Filter by Status:", ["All", "Success", "Active", "Planned", "Failed"])
    
    query = "SELECT * FROM Missions WHERE mission_name LIKE %s"
    params = [f"%{search_term}%"]
    
    if status_filter != "All":
        query += " AND status = %s"
        params.append(status_filter)
        
    df = run_query(query, tuple(params))
    st.dataframe(df, use_container_width=True)

# 2. ADD TAB
with tab_add:
    st.subheader("Add a New Mission")
    if st.session_state.role == 'admin_user':
        with st.form("add_mission_form"):
            name = st.text_input("Mission Name")
            
            # Fetch options for Foreign Keys
            agencies = run_query("SELECT agency_id, agency_name FROM Agencies")
            bodies = run_query("SELECT body_id, body_name FROM Celestial_Bodies")
            
            agency = st.selectbox("Agency", agencies['agency_name'].tolist())
            body = st.selectbox("Target Body", bodies['body_name'].tolist())
            
            m_type = st.text_input("Mission Type (e.g., Rover, Orbiter)")
            status = st.selectbox("Status", ["Planned", "Active", "Success", "Failed"])
            budget = st.number_input("Budget (Millions $)", min_value=0.0, format="%.2f")
            
            submitted = st.form_submit_button("Add Mission")
            if submitted:
                ag_id = agencies.loc[agencies['agency_name'] == agency, 'agency_id'].values[0]
                bd_id = bodies.loc[bodies['body_name'] == body, 'body_id'].values[0]
                
                insert_q = """INSERT INTO Missions (mission_name, agency_id, body_id, mission_type, status, budget_million) 
                              VALUES (%s, %s, %s, %s, %s, %s)"""
                try:
                    execute_query(insert_q, (name, int(ag_id), int(bd_id), m_type, status, float(budget)))
                    st.success("Mission added successfully! ✅")
                except Exception as e:
                    st.error(f"Error: {e} ❌")
    else:
        st.error("Permission Denied: Only Admins can add missions. ❌")

# 3. UPDATE TAB
with tab_update:
    st.subheader("Update Mission Budget/Status")
    if st.session_state.role == 'admin_user':
        missions = run_query("SELECT mission_id, mission_name FROM Missions")
        
        if not missions.empty:
            with st.form("update_mission_form"):
                target_mission = st.selectbox("Select Mission to Update", missions['mission_name'].tolist())
                new_status = st.selectbox("New Status", ["Planned", "Active", "Success", "Failed"])
                new_budget = st.number_input("New Budget (Millions $)", min_value=0.0, format="%.2f")
                
                updated = st.form_submit_button("Update")
                if updated:
                    m_id = missions.loc[missions['mission_name'] == target_mission, 'mission_id'].values[0]
                    update_q = "UPDATE Missions SET status = %s, budget_million = %s WHERE mission_id = %s"
                    try:
                        execute_query(update_q, (new_status, float(new_budget), int(m_id)))
                        st.success("Mission updated successfully! ✅")
                    except Exception as e:
                        st.error(f"Error: {e} ❌")
        else:
            st.info("No missions available to update.")
    else:
        st.error("Permission Denied: Only Admins can update missions. ❌")

# 4. DELETE TAB
with tab_delete:
    st.subheader("Delete a Mission")
    if st.session_state.role == 'admin_user':
        missions_del = run_query("SELECT mission_id, mission_name FROM Missions")
        
        if not missions_del.empty:
            with st.form("delete_mission_form"):
                del_mission = st.selectbox("Select Mission to Delete", missions_del['mission_name'].tolist())
                st.warning("Warning: This will also delete associated launches and satellites due to ON DELETE CASCADE.")
                
                deleted = st.form_submit_button("Delete Mission")
                if deleted:
                    m_id = missions_del.loc[missions_del['mission_name'] == del_mission, 'mission_id'].values[0]
                    del_q = "DELETE FROM Missions WHERE mission_id = %s"
                    try:
                        execute_query(del_q, (int(m_id),))
                        st.success("Mission deleted successfully! ✅")
                    except Exception as e:
                        st.error(f"Error: {e} ❌")
        else:
            st.info("No missions available to delete.")
    else:
        st.error("Permission Denied: Only Admins can delete missions. ❌")