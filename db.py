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
# from sqlalchemy.orm import sessionmaker

# 🔹 Cấu hình kết nối PostgreSQL LOCAL (DBeaver)

DB_CONFIG = {
    "host": "dpg-cuus8l7noe9s73an50i0-a.singapore-postgres.render.com",
    "database": "dbname_36uq",
    "user": "postgre",
    "password": "kvPtFVelp2bJrz8XbZcACaQSbnJvuI8r",
    "port": "5432"
}
# db_url = f"postgresql://postgre:kvPtFVelp2bJrz8XbZcACaQSbnJvuI8r@dpg-cuus8l7noe9s73an50i0-a.singapore-postgres.render.com/dbname_36uq"
# engine = create_engine(db_url)

# Session = sessionmaker(bind=engine)
# session = Session()

# def get_Data():
#     query = text("select * from area_code_xlsx")
#     result = session.execute(query)
#     df = pd.DataFrame(result.fetchall(), columns=result.keys())
    
#     print(df)
#     session.close()
#     return df

# print('Test1')


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

# def push_data_to_render(df, table_name="baocao_tonghop"):
#     """Đẩy dữ liệu lên PostgreSQL trên Render"""
#     try:
#         if not df.empty:
#             df.to_sql(table_name, engine, if_exists="append", index=False)
#             print(f"✅ Dữ liệu đã đẩy lên Render thành công.")
#         else:
#             print("⚠️ Không có dữ liệu để đẩy lên Render.")
#     except Exception as e:
#         print(f"❌ Lỗi khi đẩy dữ liệu lên Render: {e}")
        
        
# postgresql://postgre:Re09vjsHna84KUuedl6JMkT5FUkVsIE5@dpg-cuuic7dds78s73aviu40-a.oregon-postgres.render.com/project_0u2l