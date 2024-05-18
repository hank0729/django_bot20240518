import sqlite3
import pandas as pd

conn = sqlite3.connect('db.sqlite3')

query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql_query(query, conn)

writer = pd.ExcelWriter('database_export.xlsx', engine='openpyxl')

for table in tables['name']:
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    df.to_excel(writer, sheet_name=table, index=False)

writer.close()

conn.close()
