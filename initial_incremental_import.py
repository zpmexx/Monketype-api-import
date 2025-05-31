import requests
from dotenv import load_dotenv
from datetime import datetime
import os
import csv
import sqlite3
import json
import sys

# Import stats.py code function
from stats import runFunction

now = formatDateTime = None
try:
    now = datetime.now()
    formatDateTime = now.strftime("%d/%m/%Y %H:%M")
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""Problem with date - {str(e)}\n""")

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
    load_dotenv()
    API_KEY = os.getenv('apikey') # Personal API KEY from .env file
    db_file_path = os.getenv('db_file_path') # Path to history.db file from .env file

    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute(sql_query)
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with history.db - {e}\n""")
    sys.exit(0)
# Get latest timestamp data

# List of required db columns
db_columns = ['_id', 'wpm', 'rawWpm', 'charStats', 'acc', 'mode', 'mode2', 'consistency', 'timestamp', 'testDuration']

# When script is run for the first time, you want to get all results, but every other time you want to omit first result because of MonkeyType 'onOrAfterTimestamp' include last record from db
INSERT_FIRST = True
try:
    last_timestamp = conn.execute("SELECT MAX(timestamp) FROM typing_history").fetchone()[0]
    if last_timestamp:
        last_formated_datetime = datetime.utcfromtimestamp(last_timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
        INSERT_FIRST = False
        print(last_formated_datetime)
    else:
        last_timestamp = 1589428800000 # first acceptable timestamp by monkeytype

except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with getting last date from db - {str(e)}\n""")
    sys.exit(0)



BASE_URL = 'https://api.monkeytype.com/'

# Endpoint variables
results_endpoint = 'results'

# Headers 
headers = {
    'Authorization': f'ApeKey {API_KEY}',  
    'Content-Type': 'application/json'
}
params = {
    'onOrAfterTimestamp': last_timestamp
}

# Full url
url = BASE_URL + results_endpoint
rows_counter = inserted_to_db_rows = 0
timezone_change = 1 # add od subtract hours to GMT response (London time)
print(f'url: {url}')
print(f'last_timestamp: {last_timestamp}')
print(f'INSERT_FIRST: {INSERT_FIRST}')
try:
    # Api request
    response = requests.get(url, headers=headers, params=params)
    data = response.json()  # Parse JSON
    #print(data['data'])
    if data['data']:
        print("dlugosc data")
        print(len(data['data']))
        if INSERT_FIRST:
            without_last_data = data['data'] # Keep first record first time
        else:
            without_last_data = data['data'][:-1] # Monkeytype api fetch result with given timestamp, therefore its needed to ignore this element
        for row in without_last_data:
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
        file.write(f"""{formatDateTime} Incremental import - Problem with inserting data {e}\n""")
        

db_row_count = 0
try:
    db_row_count = cursor.execute("SELECT COUNT(*) FROM typing_history where timestamp > ?", (last_timestamp,)).fetchone()[0]
    print(f"imported: {db_row_count}")
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with SELECT query into db - {e}\n""")

try:
    with open ('import_status.log', 'a') as file:
        file.write(f"""{formatDateTime} - Init incremental Downloaded: {rows_counter} rows, Uploaded to db: {inserted_to_db_rows} rows, db rows count: {db_row_count}\n""")
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with import_status.log file - {e}\n""")
        
conn.close()