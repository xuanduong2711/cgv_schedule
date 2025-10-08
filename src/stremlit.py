from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
import pyodbc
from datetime import datetime

# Load .env
load_dotenv()

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DB = os.getenv("SQL_DB")
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")
TABLE_NAME = os.getenv("TABLE_NAME")
MOVIE_COL = os.getenv("MOVIE_COL")
DATE_COL = os.getenv("DATE_COL")

st.title("Movie Selector — Query trực tiếp từ SQL Server")

@st.cache_resource(ttl=3600)
def get_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SQL_SERVER};DATABASE={SQL_DB};UID={SQL_USER};PWD={SQL_PASSWORD}"
    )
    return pyodbc.connect(conn_str)

@st.cache_data(ttl=300)
def query_movies_and_dates():
    conn = get_connection()
    query = f"""
        SELECT DISTINCT {MOVIE_COL}, {DATE_COL}
        FROM {TABLE_NAME}
        ORDER BY {MOVIE_COL}, {DATE_COL}
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Load data
df = query_movies_and_dates()

# Parse ngày
df['_parsed_date'] = pd.to_datetime(df[DATE_COL], errors='coerce')
df['_date_only'] = df['_parsed_date'].dt.date

# Sidebar lọc
movies = ["(Tất cả)"] + sorted(df[MOVIE_COL].dropna().unique())
selected_movie = st.sidebar.selectbox("Chọn phim", movies, index=0)

dates = ["(Tất cả)"] + sorted(df['_date_only'].dropna().unique())
selected_date = st.sidebar.selectbox("Chọn ngày chiếu", dates, index=0)

# Lọc dữ liệu
filtered = df.copy()
if selected_movie != "(Tất cả)":
    filtered = filtered[filtered[MOVIE_COL] == selected_movie]

if selected_date != "(Tất cả)":
    filtered = filtered[filtered['_date_only'] == selected_date]

st.dataframe(filtered)

# Download CSV
st.download_button(
    label="Tải CSV kết quả",
    data=filtered.to_csv(index=False).encode('utf-8'),
    file_name="filtered_movies.csv",
    mime="text/csv"
)
