import csv
import sqlite3
from datetime import datetime
import sys
import json
import os
from dotenv import load_dotenv
# File name to import data
csv_file = 'results.csv'

# List of required db columns
db_columns = ['_id', 'wpm', 'rawWpm', 'charStats', 'acc', 'mode', 'mode2', 'consistency', 'timestamp', 'testDuration']

sql_query = f"""CREATE TABLE IF NOT EXISTS typing_history (
    _id TEXT PRIMARY KEY,
    wpm REAL,
    rawWpm REAL,
    charStats TEXT,
    acc REAL,
    mode TEXT,
    mode2 INTEGER,
    consistency REAL,
    timestamp INTEGER,
    testDuration REAL
);
"""

now = formatDateTime = None
try:
    now = datetime.now()
    formatDateTime = now.strftime("%d/%m/%Y %H:%M")
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""Problem with date - {str(e)}\n""")


# Sqlite connection
try:
    load_dotenv()
    API_KEY = os.getenv('apikey') # Personal API KEY from .env file
    db_file_path = os.getenv('db_file_path') # Path to history.db file from .env file
    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with history.db - {e}\n""")
    sys.exit(0)
    
inserted_to_db_rows = 0

try:
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        csv_len = len(list(csv_reader))
        if csv_len == 0:
            with open ('logfile.log', 'a') as file:
                file.write(f"""{formatDateTime} Initial csv file read - No data in csv file to import""")
        else:
            cursor.execute(sql_query)
            cursor.execute('DELETE FROM typing_history')
            
            # Set csv read file at the beginning and skip headers
            file.seek(0)
            next(csv_reader)
            
            for row in csv_reader:
            # Cast list/dict to str before inserting to db
                values = [
                    json.dumps(row[header]) if isinstance(row[header], (list, dict)) else row[header]
                    for header in db_columns  # Iterate over the db_columns
                ]
                # Insert the data into the database
                cursor.execute(f"""
                    INSERT INTO typing_history ({', '.join(db_columns)})
                    VALUES ({', '.join(['?'] * len(db_columns))})
                """, values)
                inserted_to_db_rows += 1
                
            conn.commit()
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Initial csv file read - Problem with inserting data {e}\n""")

db_row_count = 0
try:
    db_row_count = cursor.execute("SELECT COUNT(*) FROM typing_history").fetchone()
    db_row_count = db_row_count[0]
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with SELECT query into db - {e}\n""")

try:
    with open ('import_status.log', 'a') as file:
        file.write(f"""{formatDateTime} - Downloaded: {csv_len} rows, Uploaded to db: {inserted_to_db_rows} rows, db rows count: {db_row_count}\n""")
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with import_status.log file - {e}\n""")

conn.close()