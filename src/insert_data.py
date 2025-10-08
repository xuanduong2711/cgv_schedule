import pyodbc
import csv
import sys

def insert_csv_to_mssql(csv_path: str):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=sqlserver,1433;'
        'DATABASE=MovieDB;'
        'UID=sa;'
        'PWD=YourStrong!Passw0rd;'
    )
    cursor = conn.cursor()

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT INTO dbo.MovieSchedule (Theater, NameMovie, [Day], [Month], [Time])
                VALUES (?, ?, ?, ?, ?)
            """, (
                row['theater'],
                row['name_movie'],
                int(row['day']),
                int(row['month']),
                row['time']
            ))

    conn.commit()
    cursor.close()
    conn.close()

insert_csv_to_mssql(sys.argv[1])
