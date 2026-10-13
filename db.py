import mysql.connector
import pandas as pd
import streamlit as st

def get_connection():
    # Adjust user/password if your local MySQL setup requires root access
    return mysql.connector.connect(
        host="localhost",
        user="root", 
        password="8254829",
        database="space_db"
    )

def run_query(query, params=None):
    """Executes a SELECT query and returns a Pandas DataFrame."""
    conn = get_connection()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

def execute_query(query, params=None):
    """Executes INSERT, UPDATE, or DELETE commands."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()