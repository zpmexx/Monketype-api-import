import requests
from dotenv import load_dotenv
from datetime import datetime
import os
import csv
import sqlite3
import json
import sys

print("test")

# Import stats.py code function
from stats import runFunction

now = formatDateTime = None
try:
    now = datetime.now()
    formatDateTime = now.strftime("%d/%m/%Y %H:%M")
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""Problem with date - {str(e)}\n""")

# List of required db columns
db_columns = ['_id', 'wpm', 'rawWpm', 'charStats', 'acc', 'mode', 'mode2', 'consistency', 'timestamp', 'testDuration']

# Sqlite connection
try:
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with history.db - {e}\n""")
    sys.exit(0)

# Get latest timestamp data
try:
    last_timestamp = conn.execute("SELECT MAX(timestamp) FROM typing_history").fetchone()[0]
    last_formated_datetime = datetime.utcfromtimestamp(last_timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""Problem with getting last date from db - {str(e)}\n""")
    sys.exit(0)


#load env variables
load_dotenv()
API_KEY = os.getenv('apikey') # Personal API KEY from .env file

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
try:
    # Api request
    response = requests.get(url, headers=headers, params=params)
    data = response.json()  # Parse JSON
    #print(data['data'])
    if data['data']:
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
    print(db_row_count)
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with SELECT query into db - {e}\n""")

try:
    with open ('import_status.log', 'a') as file:
        file.write(f"""{formatDateTime} - Incremental Downloaded: {rows_counter} rows, Uploaded to db: {inserted_to_db_rows} rows, db rows count: {db_row_count}\n""")
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with import_status.log file - {e}\n""")
        
conn.close()

# Run stats code if there was any changes and downloaded data == imported to db data
# You delete/comment this two lines if you dont want to upload into github automatically
if rows_counter >0 and rows_counter == inserted_to_db_rows == db_row_count:
    runFunction()
