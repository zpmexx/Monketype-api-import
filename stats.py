import sqlite3
import subprocess
from datetime import datetime
import sys


now = formatDateTime = None
try:
    now = datetime.now()
    formatDateTime = now.strftime("%d/%m/%Y %H:%M")
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""Problem with date - {str(e)}\n""")

# SQL Connection
try:
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    # Select query
    cursor.execute("""
    SELECT 
        COUNT(*) AS total_count,
        AVG(wpm) AS avg_wpm,
        AVG(acc) AS avg_acc,
        MAX(wpm) AS max_wpm,
        MIN(wpm) AS min_wpm,
        STRFTIME('%H:%M:%S', SUM(testDuration), 'unixepoch') AS total_duration,
        (SELECT AVG(wpm) FROM (SELECT wpm FROM typing_history ORDER BY timestamp DESC LIMIT 10)) AS avg_wpm_last_10,
        (SELECT AVG(acc) FROM (SELECT acc FROM typing_history ORDER BY timestamp DESC LIMIT 10)) AS avg_acc_last_10,
        (SELECT MAX(wpm) FROM (SELECT wpm FROM typing_history ORDER BY timestamp DESC LIMIT 10)) AS max_wpm_last_10,
        (SELECT MIN(wpm) FROM (SELECT wpm FROM typing_history ORDER BY timestamp DESC LIMIT 10)) AS min_wpm_last_10,
        STRFTIME('%H:%M:%S', (SELECT SUM(testDuration) FROM (SELECT testDuration FROM typing_history ORDER BY timestamp DESC LIMIT 10)), 'unixepoch') AS sum_duration_last_10,
        (SELECT COUNT(*) FROM (SELECT * FROM typing_history ORDER BY timestamp DESC LIMIT 10)) AS count_last_10
    FROM typing_history;
""")

    # Fetch result
    result = cursor.fetchone()
    # Assign variables
    total_count = result[0]
    avg_wpm = result[1]
    avg_acc = result[2]
    max_wpm = result[3]
    min_wpm = result[4]
    total_duration = result[5]

    # Last 10 results stats variables
    avg_wpm_last_10 = result[6]
    avg_acc_last_10 = result[7]
    max_wpm_last_10 = result[8]
    min_wpm_last_10 = result[9]
    sum_duration_last_10 = result[10]
    count_last_10 = result[11]
    
    # Last 10 test whole data
    cursor.execute("""SELECT wpm, acc, consistency, mode || ' ' || mode2 AS mode, STRFTIME('%d-%m-%Y %H:%M:%S', timestamp / 1000, 'unixepoch')
                        from typing_history order by timestamp DESC LIMIT 10 """)
    
    result = cursor.fetchall()
    markdown_last_10_table = None
    if result:
        markdown_last_10_table = "### Last 10 results\n\n"
        markdown_last_10_table += "| WPM | Accuracy | Consistency | Mode | Date |\n"
        markdown_last_10_table += "| --- | -------- | ----------- | ---- | --------- |\n"
        # Populate table rows dynamically
        for row in result:
            markdown_last_10_table += f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} |\n"
        markdown_last_10_table += "\n\n --- \n\n"
    
    # Top 10 test whole data
    cursor.execute("""SELECT wpm, acc, consistency, mode || ' ' || mode2 AS mode, STRFTIME('%d-%m-%Y %H:%M:%S', timestamp / 1000, 'unixepoch')
                        from typing_history order by wpm DESC LIMIT 10 """)
    
    result = cursor.fetchall()
    markdown_top_10_table = None
    if result:
        markdown_top_10_table = "### Top 10 results\n\n"
        markdown_top_10_table += "| WPM | Accuracy | Consistency | Mode | Date |\n"
        markdown_top_10_table += "| --- | -------- | ----------- | ---- | --------- |\n"
    
        
        # Populate table rows dynamically
        for row in result:
            markdown_top_10_table += f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} |\n"
        markdown_top_10_table += "\n\n --- \n\n"
    # Close db connection
    conn.close()
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with reading data from db - {str(e)}\n""")
        
    # Close db connecton in case of error
    conn.close()
    # End program
    sys.exit() 

        
# Readme content update
try:
    markdown_table = f"""
[Configuration](#configuration)
## Typing History Stats (Last Updated: {formatDateTime})

| **Key Stats**               | **Overall Stats**       | **Last 10 Tests Stats**  |
|--------------------------|-------------------------|--------------------------|
| **Total Entries**        | {total_count}           | {sum_duration_last_10}                       |
| **Average WPM**          | {avg_wpm:.2f}           | {avg_wpm_last_10:.2f}    |
| **Average Accuracy**     | {avg_acc:.2f}%          | {avg_acc_last_10:.2f}%   |
| **Max WPM**              | {max_wpm}               | {max_wpm_last_10}        |
| **Min WPM**              | {min_wpm}               | {min_wpm_last_10}                        |
| **Total Duration**       | {total_duration}        | {count_last_10}                        |


---

"""
    if markdown_last_10_table:
        markdown_table += markdown_last_10_table
        
    if  markdown_top_10_table:
        markdown_table +=  markdown_top_10_table
   
    configuration_markdown = f"""
# Configuration

1. **Get API Key from account settings -> ape keys -> generate new key**
2. **Add generated api key to .env file variable apikey**
3. **Run get_data.py script that will load data from [Monkeytype](https://monkeytype.com/) and insert into sqllite3 db history.db (this wont be stored on your GitHub)**
4. **Error logs will be stored into logfile.log, and import status will be stored into import_status.log**
5. **stats.py script will get data from db and push them into GitHub account**
    
    """
    
    
    markdown_table += configuration_markdown
    
    with open("README.md", "w") as file:
        file.write(markdown_table)
        
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with markdown content - {str(e)}\n""")
        
        
# Push readme file to github
try:
    subprocess.run(["git", "add", "README.md"])  # Add the README file to git
    subprocess.run(["git", "commit", "-m", f"Update README with new stats ({formatDateTime})"])  # Commit the change
    
    # Set branch to main/master or specific
    branch = 'master'
    subprocess.run(["git", "push", "origin", branch])  # Push to the specific branch
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with pushing data into GitHub account - {str(e)}\n""")