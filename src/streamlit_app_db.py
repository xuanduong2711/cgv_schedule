import streamlit as st
import pyodbc
import os
from dotenv import load_dotenv
import pandas as pd

# --- Cấu hình trang và Tải biến môi trường ---
st.set_page_config(layout="wide", page_title="Lịch Chiếu Phim")
load_dotenv()

# --- Tối ưu kết nối và Tải dữ liệu ---

# Dùng st.cache_resource để tạo kết nối DB một lần duy nhất và tái sử dụng.
# Điều này giúp tăng tốc độ và tránh mở quá nhiều kết nối không cần thiết.
@st.cache_resource
def get_connection():
    """Tạo và cache kết nối đến SQL Server."""
    server = os.getenv("SQL_SERVER")
    database = os.getenv("SQL_DB")
    username = os.getenv("SQL_USER")
    password = os.getenv("SQL_PASSWORD")
    
    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"TrustServerCertificate=yes;"
    )
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as ex:
        st.error(f"Lỗi kết nối đến cơ sở dữ liệu! Vui lòng kiểm tra lại cấu hình.")
        st.exception(ex)
        return None

# Dùng st.cache_data để tải dữ liệu từ DB một lần và lưu vào cache.
# Lần sau khi cần dữ liệu, Streamlit sẽ lấy từ cache thay vì query lại DB.
@st.cache_data
def load_data(_conn):
    """Tải toàn bộ dữ liệu lịch chiếu phim từ database."""
    if _conn:
        # Thay đổi tên bảng tại đây cho khớp với database của bạn
        table_name = os.getenv("TABLE_NAME", "Movie_cgv") 
        query = f"SELECT * FROM dbo.{table_name}"
        df = pd.read_sql(query, _conn)
        return df
    return pd.DataFrame()

# --- Giao diện ứng dụng ---
st.title("🎬 Lịch Chiếu Phim")

conn = get_connection()

if conn:
    df = load_data(conn)

    if df.empty:
        st.warning("Không có dữ liệu nào trong database hoặc không thể tải dữ liệu.")
    else:
        # --- BỘ LỌC Ở THANH BÊN (SIDEBAR) ---
        st.sidebar.header("Bộ lọc 🔎")

        # 1. Lọc theo rạp chiếu phim
        # SỬA LỖI: Đổi 'Theater' thành 'theater' (viết thường)
        theaters = sorted(df['theater'].unique().tolist())
        # Thêm tùy chọn "Tất cả" vào đầu danh sách
        selected_theater = st.sidebar.selectbox(
            "Chọn rạp:",
            options=["Tất cả"] + theaters
        )

        # 2. Tìm kiếm theo tên phim
        search_movie = st.sidebar.text_input("Tìm kiếm theo tên phim:")

        # --- Xử lý lọc dữ liệu ---
        # Bắt đầu với DataFrame đầy đủ
        filtered_df = df

        # Áp dụng bộ lọc rạp
        if selected_theater != "Tất cả":
            # SỬA LỖI: Đổi 'Theater' thành 'theater' (viết thường)
            filtered_df = filtered_df[filtered_df['theater'] == selected_theater]

        # Áp dụng bộ lọc tìm kiếm tên phim
        if search_movie:
            # SỬA LỖI: Đổi 'NameMovie' thành 'name_movie' (viết thường)
            # .str.contains() để tìm chuỗi con, case=False để không phân biệt hoa thường
            filtered_df = filtered_df[filtered_df['name_movie'].str.contains(search_movie, case=False, na=False)]

        # --- Hiển thị kết quả ---
        st.subheader(f"Tìm thấy {len(filtered_df)} suất chiếu")
        
        # Hiển thị DataFrame đã được lọc
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

