import sqlite3
import subprocess
from datetime import datetime
import sys
import os
from charts import create_and_export_charts

def runFunction():
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
        counter = 0
        if result:
            markdown_last_10_table = "### Last 10 results\n\n"
            markdown_last_10_table += "| | WPM | Accuracy | Consistency | Mode | Date |\n"
            markdown_last_10_table += "| --- | --- | -------- | ----------- | ---- | --------- |\n"
            # Populate table rows dynamically
            for row in result:
                counter += 1
                markdown_last_10_table += f"| {counter} | {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} |\n"
            markdown_last_10_table += "\n\n --- \n\n"
        
        # Top 10 test whole data
        cursor.execute("""SELECT wpm, acc, consistency, mode || ' ' || mode2 AS mode, STRFTIME('%d-%m-%Y %H:%M:%S', timestamp / 1000, 'unixepoch')
                            from typing_history order by wpm DESC LIMIT 10 """)
        
        result = cursor.fetchall()
        markdown_top_10_table = None
        counter = 0
        if result:
            markdown_top_10_table = "### Top 10 results\n\n"
            markdown_top_10_table += "| | WPM | Accuracy | Consistency | Mode | Date |\n"
            markdown_top_10_table += "| --- | --- | -------- | ----------- | ---- | --------- |\n"
        
            
            # Populate table rows dynamically
            for row in result:
                counter +=1
                markdown_top_10_table += f"| {counter} | {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} |\n"
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

    
    profile_name = 'zp14' # set your public profile name
    
    if profile_name:
        markdown_table = f"""
[Configuration](#configuration)
## My public Monkeytype [profile](https://monkeytype.com/profile/{profile_name})\n\n
        """
    else:
        markdown_table = f""" 
[Configuration](#configuration)
        """     
    
    try:
        create_and_export_charts()
    except Exception as e:
        with open ('logfile.log', 'a') as file:
            file.write(f"""{formatDateTime} Problem with creating charts - {str(e)}\n""")
    # Readme content update
    try:
        markdown_table += f"""
## Typing History Stats (Last Updated: {formatDateTime})

| **Key Stats**               | **Overall Stats**       | **Last 10 Tests Stats**  |
|--------------------------|-------------------------|--------------------------|
| **Total Entries**        | {total_count}           | {count_last_10}                       |
| **Average WPM**          | {avg_wpm:.2f}           | {avg_wpm_last_10:.2f}    |
| **Average Accuracy**     | {avg_acc:.2f}%          | {avg_acc_last_10:.2f}%   |
| **Max WPM**              | {max_wpm}               | {max_wpm_last_10}        |
| **Min WPM**              | {min_wpm}               | {min_wpm_last_10}                        |
| **Total Duration**       | {total_duration}        | {sum_duration_last_10}                        |


---

"""
        if markdown_last_10_table:
            markdown_table += markdown_last_10_table
            
        if  markdown_top_10_table:
            markdown_table +=  markdown_top_10_table
    
        configuration_markdown = f"""
        
![speed trend](typing_speed_trend.png)
![counted chart](count_tests.png)
# Configuration

1. **Get API Key from account settings -> ape keys -> generate new key -> check active button next to apekey's name**
2. **Add generated api key to .env file variable apikey**
3. **Install modules** `pip install -r req.txt`
3. **(If you've got less than 1000 tests completed) Run get_data_max_1000.py script that will load data from [Monkeytype](https://monkeytype.com/) and insert into sqllite3 db history.db (this wont be stored on your GitHub)**
4. **Error logs will be stored into logfile.log, and import status will be stored into import_status.log**
5. **stats.py script will get data from db and push them into GitHub account**
6. **You can use API call via ApeKey 30 times per day, so after you reach this limit you wont get any answear and in logfile you will see *Problem with inserting data 0* row**
7. **incremental_import.py will check for the last result time in db and download just those tests that are younger than that. It will also update automatically into GitHub account unless you comment last 2 line of code.**

# UPDATE for 1000+ tests
    
**As monkeytype API enables just 1000 rows to be downloaded via API call, for proper inintial insertion to db tests where there are more than 1000 on your profile
you should export csv file from [Monkeytype account](https://monkeytype.com/account) (over results at the bottom of the site)
and put this csv file into project folder (or set proper path to this file into variable csv_file), then run inintial_csv_read.py script.**
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
        typing_speed_chart_file = "typing_speed_trend.png"
        count_tests_chart_file = "count_tests.png"
        if os.path.exists(typing_speed_chart_file):
            subprocess.run(["git", "add", "typing_speed_trend.png"])
        if os.path.exists(count_tests_chart_file):
            subprocess.run(["git", "add", "count_tests.png"])
        
        subprocess.run(["git", "commit", "-m", f"Update README with new stats ({formatDateTime})"])  # Commit the change
        
        # Set branch to main/master or specific
        branch = 'master'
        subprocess.run(["git", "push", "origin", branch])  # Push to the specific branch
    except Exception as e:
        with open ('logfile.log', 'a') as file:
            file.write(f"""{formatDateTime} Problem with pushing data into GitHub account - {str(e)}\n""")

if __name__ == "__main__":
    runFunction()