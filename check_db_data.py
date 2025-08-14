import sqlite3
import os
from config import Config

def check_database_data():
    # 确定数据库路径
    db_path = Config.INSTANCE_DIR / 'dev.db'
    print(f"数据库路径: {db_path}")
    
    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 查询所有表名
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("数据库中的表:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # 遍历所有表，查询所有字段和记录
    for table in tables:
        table_name = table[0]
        print(f"\n{table_name}表数据:")
        
        # 查询表的所有字段信息
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        
        # 查询表的所有数据
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        
        # 打印表头
        header = "  " + ", ".join(column_names)
        print(header)
        
        # 打印所有记录
        for row in rows:
            record = "  " + ", ".join(str(value) for value in row)
            print(record)
    
    # 关闭连接
    conn.close()

if __name__ == '__main__':
    check_database_data()