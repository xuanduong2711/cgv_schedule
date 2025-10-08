import os
import glob
import logging
import pyodbc
import pandas as pd

# --- Cấu hình Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_insertion():
    """
    Tìm tất cả các file part-*.csv, gộp chúng, và chèn dữ liệu vào database.
    Script này đã được sửa để xử lý file CSV có dòng tiêu đề.
    """
    conn = None
    try:
        # --- 1. Lấy cấu hình từ biến môi trường ---
        server = os.getenv("SQL_SERVER")
        database = os.getenv("SQL_DB")
        user = os.getenv("SQL_USER")
        password = os.getenv("SQL_PASSWORD", "")
        table_name = os.getenv("TABLE_NAME", "Movie_cgv")

        # --- 2. Đọc và xử lý dữ liệu từ các file CSV ---
        csv_path_pattern = '/opt/airflow/data/output/part*.csv'
        all_csv_files = glob.glob(csv_path_pattern)

        if not all_csv_files:
            logging.warning(f"Không tìm thấy file CSV nào khớp với mẫu: '{csv_path_pattern}'")
            return

        logging.info(f"Đã tìm thấy {len(all_csv_files)} file CSV. Đang đọc và gộp dữ liệu...")

        # SỬA LỖI: Bỏ 'header=None' và 'names' để pandas tự động
        # nhận diện dòng đầu tiên là dòng tiêu đề.
        df_list = [pd.read_csv(file) for file in all_csv_files]
        combined_df = pd.concat(df_list, ignore_index=True)

        if combined_df.empty:
            logging.info("Dữ liệu rỗng sau khi gộp. Không có gì để chèn.")
            return

        # --- 3. Kết nối và chèn dữ liệu vào Database ---
        conn_str = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={user};"
            f"PWD={password};"
            f"TrustServerCertificate=yes;"
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        logging.info("✅ Kết nối tới database thành công.")

        insert_query = f"""
        INSERT INTO dbo.{table_name} (theater, name_movie, [day], [month], [time])
        VALUES (?, ?, ?, ?, ?)
        """
        
        # Chuyển đổi DataFrame thành danh sách các tuple để chèn hiệu quả
        # Đảm bảo tên cột trong CSV là 'theater', 'name_movie', v.v. (viết thường)
        data_to_insert = [tuple(row) for row in combined_df[['theater', 'name_movie', 'day', 'month', 'time']].itertuples(index=False)]
        
        logging.info(f"Chuẩn bị chèn {len(data_to_insert)} bản ghi...")
        
        cursor.executemany(insert_query, data_to_insert)
        conn.commit()
        
        logging.info(f"✅ Gửi lệnh chèn dữ liệu thành công.")

    except pyodbc.Error as db_error:
        logging.error(f"Lỗi Database: {db_error}")
        if conn:
            conn.rollback()
    except KeyError as key_error:
        logging.error(f"Lỗi Tên Cột: Không tìm thấy cột {key_error} trong file CSV. Vui lòng kiểm tra lại dòng tiêu đề.")
    except Exception as e:
        logging.error(f"Đã có lỗi không xác định xảy ra: {e}")
    finally:
        if conn:
            conn.close()
            logging.info("Đã đóng kết nối database.")

if __name__ == "__main__":
    run_insertion()

