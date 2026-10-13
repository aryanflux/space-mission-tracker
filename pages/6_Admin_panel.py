import streamlit as st
import pandas as pd
from db import get_connection

# --- AUTHENTICATION CHECK ---
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in from the Home Dashboard first.")
    st.stop()

st.title("⚙️ Admin Panel: Live SQL Demo")
st.sidebar.markdown(f"**👤 User:** {st.session_state.username}")
st.sidebar.markdown(f"**🛡️ Role:** {st.session_state.role}")

# --- ROLE RESTRICTION ---
if st.session_state.role != 'admin_user':
    st.error("Permission Denied: Only Admins can access the live SQL panel. ❌")
    st.stop()

st.markdown("Execute live **DDL** (CREATE, ALTER, DROP) and **DCL** (GRANT, REVOKE) commands for your presentation demo.")

# --- SQL TEXT BOX ---
query = st.text_area("Enter SQL Command:", height=150, placeholder="e.g., SHOW GRANTS FOR 'control_user'@'localhost';")

if st.button("Execute Command"):
    if query.strip():
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query)
            
            # Catch queries that return tabular data (SELECT, SHOW)
            if query.strip().upper().startswith(("SELECT", "SHOW")):
                columns = [col[0] for col in cursor.description]
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=columns)
                st.dataframe(df, use_container_width=True)
                st.success("Query executed and results fetched successfully! ✅")
            else:
                # Catch queries that modify the database (DDL, DML, DCL)
                conn.commit()
                st.success("Command executed successfully! ✅")
            
            conn.close()
        except Exception as e:
            st.error(f"Error: {e} ❌")
    else:
        st.warning("Please enter a valid SQL command.")