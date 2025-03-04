import sqlite3
import pandas as pd
import os

TABLE_PARAMETER = "{TABLE_PARAMETER}"
DROP_TABLE_SQL = f"DROP TABLE {TABLE_PARAMETER};"
GET_TABLES_SQL = "SELECT name FROM sqlite_schema WHERE type='table';"

def delete_all_tables(con):
    tables = get_tables(con)
    delete_tables(con, tables)

def get_tables(con):
    cur = con.cursor()
    cur.execute(GET_TABLES_SQL)
    tables = cur.fetchall()
    cur.close()
    return tables

def delete_tables(con, tables):
    cur = con.cursor()
    for table, in tables:
        sql = DROP_TABLE_SQL.replace(TABLE_PARAMETER, table)
        cur.execute(sql)
    cur.close()

def ingest():
    con = sqlite3.connect("sql-db/property.db")
    # Drop all tables
    delete_all_tables(con)

    csv_dir = "knowledge/csv"
    filenames = os.listdir(csv_dir)
    filenames = [f for f in filenames if f.endswith(".csv")]

    for filename in filenames:
        print(f"Ingesting - {filename}")
        df = pd.read_csv(os.path.join(csv_dir, filename))
        tablename = filename.replace(".csv","").lower()
        df.columns = [c.lower().strip().replace(" ","_") for c in df.columns]
        df.to_sql(name=tablename, con=con)
        print(f"{filename} ingestion completed")
        print(f"{tablename} - {tuple(list(df.columns))}")

if __name__ == '__main__':
    ingest()