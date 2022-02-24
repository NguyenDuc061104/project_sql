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
from sqlalchemy import create_engine

# 🔹 Cấu hình kết nối PostgreSQL LOCAL (DBeaver)
DB_CONFIG = {
    "host": "localhost",
    "database": "project",
    "user": "postgres",
    "password": "ducan06112004",
    "port": "5432"
}

# 🔹 Kết nối PostgreSQL trên Render (Lấy từ biến môi trường)
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def get_data_from_postgres(month, table_name="baocao_tonghop"):
    """Lấy dữ liệu từ PostgreSQL LOCAL sau khi gọi Store Procedure"""
    try:
        # Kết nối PostgreSQL LOCAL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 🔹 Gọi Stored Procedure (chạy theo tháng)
        cursor.execute("CALL backdate_month(%s)", (month,))
        conn.commit()

        # 🔹 Lấy dữ liệu từ bảng
        cursor.execute(f"SELECT * FROM {table_name}")
        result = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]

        # Đóng kết nối
        cursor.close()
        conn.close()

        return pd.DataFrame(result, columns=col_names)
    
    except Exception as e:
        print(f"❌ Lỗi khi truy vấn PostgreSQL LOCAL: {e}")
        return pd.DataFrame()

def push_data_to_render(df, table_name="baocao_tonghop"):
    """Đẩy dữ liệu lên PostgreSQL trên Render"""
    try:
        if not df.empty:
            df.to_sql(table_name, engine, if_exists="append", index=False)
            print(f"✅ Dữ liệu đã đẩy lên Render thành công.")
        else:
            print("⚠️ Không có dữ liệu để đẩy lên Render.")
    except Exception as e:
        print(f"❌ Lỗi khi đẩy dữ liệu lên Render: {e}")