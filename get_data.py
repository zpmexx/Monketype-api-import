import requests
from dotenv import load_dotenv
from datetime import datetime
import os
import csv
import sqlite3
import json

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
limit = 1000 # Max limit of data per API Call is 1000
params = {
    #'mode': 'time'  # Necessary for specific endpoints
    'limit': limit
}

# Full url
url = BASE_URL + results_endpoint
#print(url)

#print(response)

# Sql table create query
sql_query = f"""CREATE TABLE IF NOT EXISTS typing_history (
    _id TEXT PRIMARY KEY,
    uid TEXT,
    wpm REAL,
    rawWpm REAL,
    charStats TEXT,
    acc REAL,
    mode TEXT,
    mode2 INTEGER,
    timestamp INTEGER,
    testDuration REAL,
    consistency REAL,
    keyConsistency REAL,
    chartData TEXT,  -- Store entire JSON as TEXT
    name TEXT,
    keySpacingStats TEXT,
    keyDurationStats TEXT
);
"""

# Sqlite connection
conn = sqlite3.connect('history.db')
cursor = conn.cursor()

# Rows counter variable
rows_counter = inserted_to_db_rows = 0
offset = 0
initial_db_clear = True
# Get data
try:
    while True:
        params['offset'] = offset # Add offset to params
        # Api request
        response = requests.get(url, headers=headers, params=params)
        data = response.json()  # Parse JSON
        if data['data']:
            #print(data['data'])
            # Delete data from db
            if initial_db_clear:
                cursor.execute(sql_query)
                cursor.execute('DELETE FROM typing_history')
                initial_db_clear = False
                
            # Get headers
            headers_row = data['data'][0].keys() 
            for row in data['data']: 
                rows_counter+=1
                # Cast list/dict to str before inserting to db
                values = [
                json.dumps(row[header]) if isinstance(row[header], (list,dict)) else row[header]
                for header in headers_row
            ]
                # Insert into db
                cursor.execute(f'''
                    INSERT INTO typing_history ({', '.join(headers_row)})
                    VALUES ({', '.join(['?'] * len(headers_row))})
                ''', values)
                inserted_to_db_rows += 1
            
            # Commit changes
            conn.commit()
            offset += limit # Move forward with data
        else:
            break
        
    # Get db rows count
    db_row_count = 0
    try:
        db_row_count = cursor.execute("SELECT COUNT(*) FROM typing_history").fetchone()
        db_row_count = db_row_count[0]
    except Exception as e:
        with open ('logfile.log', 'a') as file:
            file.write(f"""{formatDateTime} Problem with SELECT query into db - {e}\n""")
    
    conn.close()
    with open ('import_status.log', 'a') as file:
        file.write(f"""{formatDateTime} - Downloaded: {rows_counter} rows, Uploaded to db: {inserted_to_db_rows} rows, db rows count: {db_row_count}\n""")
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with inserting data {e}\n""")

