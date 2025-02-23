# import psycopg2
# import pandas as pd

# # Cấu hình kết nối PostgreSQL
# DB_CONFIG = {
#     "host": "localhost",
#     "database": "project",
#     "user": "postgres",
#     "password": "ducan06112004",
#     "port": "5432"
# }

# def get_data_from_postgres(month, table_name="baocao_tonghop"):
#     """Lấy dữ liệu từ PostgreSQL sau khi gọi Store Procedure"""
#     try:
#         conn = psycopg2.connect(**DB_CONFIG)
#         cursor = conn.cursor()
#         cursor.execute("CALL backdate_month(%s)", (month,))
#         conn.commit()
#         cursor.execute(f"SELECT * FROM {table_name}")
#         result = cursor.fetchall()
#         col_names = [desc[0] for desc in cursor.description]
#         cursor.close()
#         conn.close()
#         return pd.DataFrame(result, columns=col_names)
#     except Exception as e:
#         print(f"Lỗi PostgreSQL: {e}")
#         return pd.DataFrame()
import os
import psycopg2
import pandas as pd

# Lấy DATABASE_URL từ biến môi trường (đã đặt trong Render)
DATABASE_URL = os.getenv("DATABASE_URL")

def get_data_from_postgres(month, table_name="baocao_tonghop"):
    """Lấy dữ liệu từ PostgreSQL sau khi gọi Store Procedure"""
    try:
        # Kết nối PostgreSQL bằng DATABASE_URL từ biến môi trường
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Gọi Store Procedure
        cursor.execute("CALL backdate_month(%s)", (month,))
        conn.commit()

        # Lấy dữ liệu từ bảng
        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]

        # Đóng kết nối
        cursor.close()
        conn.close()

        return pd.DataFrame(result, columns=col_names)
    
    except Exception as e:
        print(f"❌ Lỗi PostgreSQL: {e}")
        return pd.DataFrame()
