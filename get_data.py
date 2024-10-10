import requests
from dotenv import load_dotenv
from datetime import datetime
import os

#load env variables
load_dotenv()
API_KEY = os.getenv('apikey') # Personal API KEY from .env file
now = formatDateTime = None
try:
    now = datetime.now()
    formatDateTime = now.strftime("%d/%m/%Y %H:%M")
except Exception as e:
    pass

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

# Api request
response = requests.get(url, headers=headers, params=params)


# Get data

try:
    data = response.json()  # Parse JSON
    with open ("result.txt", 'wb') as file:
        for row in response:
            file.write(row)
            
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{str(e)}\n""")

