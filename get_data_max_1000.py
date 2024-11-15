import requests
from dotenv import load_dotenv
from datetime import datetime
import os
import csv
import sqlite3
import json
import sys
#load env variables
load_dotenv()
API_KEY = os.getenv('apikey') # Personal API KEY from .env file

now = formatDateTime = None
try:
    now = datetime.now()
    formatDateTime = now.strftime("%d/%m/%Y %H:%M")
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""Problem with date - {str(e)}\n""")

# Base URL for Monkeytype API
BASE_URL = 'https://api.monkeytype.com/'

# Endpoint variables
last_result_endpoint = 'results/last'
personal_best_endpoint = 'users/personalBests'
results_endpoint = 'results'

# Headers 
headers = {
    'Authorization': f'ApeKey {API_KEY}',  
    'Content-Type': 'application/json'
}
params = {
    #'mode': 'time'  # Necessary for specific endpoints
}

# Full url
url = BASE_URL + results_endpoint
#print(url)

#print(response)

# Sql table create query
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

# Sqlite connection
try:
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with history.db - {e}\n""")
    sys.exit(0)


# Rows counter variable
rows_counter = inserted_to_db_rows = 0
# Get data
db_columns = ['_id', 'wpm', 'rawWpm', 'charStats', 'acc', 'mode', 'mode2', 'timestamp', 'testDuration', 'consistency']

try:
    # Api request
    response = requests.get(url, headers=headers, params=params)
    data = response.json()  # Parse JSON
    print(len(data['data']))
    if data['data']:
        # Delete data from db
        cursor.execute(sql_query)
        cursor.execute('DELETE FROM typing_history')
        initial_db_clear = False
            
        for row in data['data']: 
            rows_counter+=1
            # Cast list/dict to str before inserting to db
            values = [
            json.dumps(row[header]) if isinstance(row[header], (list,dict)) else row[header]
            for header in db_columns
        ]   
            # Insert into db
            cursor.execute(f'''
                INSERT INTO typing_history ({', '.join(db_columns)})
                VALUES ({', '.join(['?'] * len(db_columns))})
            ''', values)
            inserted_to_db_rows += 1
        
        # Commit changes
        conn.commit()
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with inserting data {e}\n""")

# Get db rows count
db_row_count = 0
try:
    db_row_count = cursor.execute("SELECT COUNT(*) FROM typing_history").fetchone()
    db_row_count = db_row_count[0]
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with SELECT query into db - {e}\n""")

try:
    with open ('import_status.log', 'a') as file:
        file.write(f"""{formatDateTime} - Downloaded: {rows_counter} rows, Uploaded to db: {inserted_to_db_rows} rows, db rows count: {db_row_count}\n""")
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with import_status.log file - {e}\n""")

conn.close()