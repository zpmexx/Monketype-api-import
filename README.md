
[Configuration](#configuration)

## Typing History Stats (Last Updated: 13/11/2024 14:41)

<center>

| **Key Stats**               | **Overall Stats**       | **Last 10 Tests Stats**  |
|--------------------------|-------------------------|--------------------------|
| **Total Entries**        | 860           | 00:05:00                       |
| **Average WPM**          | 102.75           | 111.54    |
| **Average Accuracy**     | 90.86%          | 93.43%   |
| **Max WPM**              | 129.13               | 119.98        |
| **Min WPM**              | 64.77               | 99.15                        |
| **Total Duration**       | 07:11:06        | 10                        |

</center>
---

### Last 10 results

| WPM | Accuracy | Consistency | Mode | Date |
| --- | -------- | ----------- | ---- | --------- |
| 107.19 | 93.65 | 87.28 | time 30 | 12-11-2024 17:15:29 |
| 111.57 | 94.94 | 84.55 | time 30 | 12-11-2024 17:12:09 |
| 99.15 | 87.22 | 80.72 | time 30 | 12-11-2024 17:11:15 |
| 119.98 | 95.15 | 81.67 | time 30 | 12-11-2024 17:10:21 |
| 115.2 | 96.42 | 86.72 | time 30 | 12-11-2024 17:09:21 |
| 108.0 | 88.92 | 86.33 | time 30 | 12-11-2024 17:08:27 |
| 113.6 | 95.47 | 87.94 | time 30 | 12-11-2024 17:07:07 |
| 112.38 | 93.33 | 86.36 | time 30 | 12-11-2024 17:06:32 |
| 115.57 | 93.95 | 87.73 | time 30 | 12-11-2024 16:45:12 |
| 112.78 | 95.22 | 89.91 | time 30 | 12-11-2024 16:43:14 |


 --- 

### Top 10 results

| WPM | Accuracy | Consistency | Mode | Date |
| --- | -------- | ----------- | ---- | --------- |
| 129.13 | 97.93 | 87.46 | time 30 | 20-07-2024 16:54:21 |
| 126.37 | 99.08 | 86.0 | time 30 | 05-08-2024 14:25:56 |
| 125.96 | 95.82 | 86.11 | time 30 | 09-08-2024 12:56:13 |
| 125.55 | 98.18 | 85.59 | time 30 | 09-10-2024 16:32:56 |
| 124.78 | 99.06 | 87.92 | time 30 | 02-11-2024 18:46:45 |
| 123.56 | 97.56 | 87.97 | time 30 | 16-08-2024 16:52:42 |
| 123.15 | 96.98 | 84.75 | time 30 | 28-06-2024 17:01:24 |
| 123.14 | 96.95 | 86.04 | time 30 | 20-08-2024 17:01:55 |
| 122.79 | 94.38 | 87.25 | time 30 | 25-07-2024 13:09:46 |
| 122.77 | 97.81 | 82.32 | time 30 | 26-07-2024 13:50:05 |


 --- 


# Configuration

1. **Get API Key from account settings -> ape keys -> generate new key**
2. **Add generated api key to .env file variable apikey**
3. **Run get_data.py script that will load data from [Monkeytype](https://monkeytype.com/) and insert into sqllite3 db history.db (this wont be stored on your GitHub)**
4. **Error logs will be stored into logfile.log, and import status will be stored into import_status.log**
5. **stats.py script will get data from db and push them into GitHub account**
6. **You can use API call via ApeKey 30 times per day, so after you reach this limit you wont get any answear and in logfile you will see *Problem with inserting data 0* row**
    
    