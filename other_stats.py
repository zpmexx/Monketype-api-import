import sqlite3
import subprocess
from datetime import datetime
import sys
import os
from charts import create_and_export_charts
from config import other_stats

def connect_db():
    try:
        conn = sqlite3.connect('history.db')
        return conn
    except Exception as e:
        with open ('logfile.log', 'a') as file:
            file.write(f"""Problem with history.db - {e}\n""")
        sys.exit(0)

def checkModesTime(conn):
    sql_query = f"""
    SELECT mode, mode2, count(testDuration),   
  CAST(SUM(testDuration) / 3600 AS INTEGER) AS hours,
  CAST((SUM(testDuration) % 3600) / 60 AS INTEGER) AS minutes,
  CAST(SUM(testDuration) % 60 AS INTEGER) AS seconds
  FROM typing_history th GROUP BY mode, mode2 ORDER BY sum(testDuration) desc
    """
    config_text = f"""[Modes](#check-modes)\n\n"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        cursor.close()  

    except Exception as e:
        with open ('logfile.log', 'a') as file:
            file.write(f"""Problem with getting modes time - {str(e)}\n""")

    if results:
        content = ''
        counter = 0
        content += f"## All modes played and their times\n\n"
        content += "| | Mode1 | Mode2 | Tests  | Hours | Minutes | Seconds |\n"
        content += "| --- | --- | --- | ----- | ----- | ------- | ------- |\n"

        for row in results:
            counter += 1
            content += f"| {counter} | {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} |\n"
        
        content += "\n\n --- \n\n"

        return config_text, content
    
    
    
conn = connect_db()
config_all = '# Legend\n'
content_all = ''
config_text, content = checkModesTime(conn)

config_all += config_text
content_all += content


with open("other stats\other_stats.md", "w") as file:
    file.write(config_all)
    file.write(content_all)