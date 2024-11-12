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
        STRFTIME('%H:%M:%S', (SELECT SUM(testDuration) FROM (SELECT testDuration FROM typing_history ORDER BY timestamp DESC LIMIT 10)), 'unixepoch') AS sum_duration_last_10
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

    # Last 10 results variables
    avg_wpm_last_10 = result[6]
    avg_acc_last_10 = result[7]
    max_wpm_last_10 = result[8]
    min_wpm_last_10 = result[9]
    sum_duration_last_10 = result[10]
    
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
## Typing History Stats (Last Updated: {formatDateTime})

| **Metric**               | **Overall Stats**       | **Last 10 Tests Stats**  |
|--------------------------|-------------------------|--------------------------|
| **Total Entries**        | {total_count}           | 10                       |
| **Average WPM**          | {avg_wpm:.2f}           | {avg_wpm_last_10:.2f}    |
| **Average Accuracy**     | {avg_acc:.2f}%          | {avg_acc_last_10:.2f}%   |
| **Max WPM**              | {max_wpm}               | {max_wpm_last_10}        |
| **Min WPM**              | {min_wpm}               | {min_wpm_last_10}                        |
| **Total Duration**       | {total_duration}        | {sum_duration_last_10}                        |


---

### Key Insights
- **Entries Count**: {total_count} typing tests have been recorded.
- **Performance**: Your average typing speed is {avg_wpm:.2f} WPM with an accuracy of {avg_acc:.2f}%.
- **Best Performance**: The fastest WPM recorded is {max_wpm}.
- **Slowest Performance**: The lowest WPM recorded is {min_wpm}.
- **Total Time Spent**: You've spent a total of **{total_duration}** typing.

This summary gives you a historical overview and a snapshot of your recent results for easy comparison.
"""


    with open("README.md", "w") as file:
        file.write(markdown_table)
        
except Exception as e:
    with open ('logfile.log', 'a') as file:
        file.write(f"""{formatDateTime} Problem with markdown content - {str(e)}\n""")
        
        
# # Push readme file to github
# try:
#     subprocess.run(["git", "add", "README.md"])  # Add the README file to git
#     subprocess.run(["git", "commit", "-m", f"Update README with new stats ({formatDateTime})"])  # Commit the change
    
#     # Set branch to main/master or specific
#     branch = 'master'
#     subprocess.run(["git", "push", "origin", branch])  # Push to the specific branch
# except Exception as e:
#     with open ('logfile.log', 'a') as file:
#         file.write(f"""{formatDateTime} Problem with pushing data into GitHub account - {str(e)}\n""")