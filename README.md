
# [Configuration](#configuration)
## Typing History Stats (Last Updated: 13/11/2024 13:30)

| **Metric**               | **Overall Stats**       | **Last 10 Tests Stats**  |
|--------------------------|-------------------------|--------------------------|
| **Total Entries**        | 850           | 00:05:00                       |
| **Average WPM**          | 102.64           | 102.19    |
| **Average Accuracy**     | 90.83%          | 90.07%   |
| **Max WPM**              | 129.13               | 114.38        |
| **Min WPM**              | 64.77               | 89.98                        |
| **Total Duration**       | 07:06:06        | 10                        |


---

### Last 10 results

| WPM | Accuracy | Consistency | Mode | Timestamp |
| --- | -------- | ----------- | ---- | --------- |
| 91.57 | 87.3 | 85.58 | time 30 | 11-11-2024 12:13:15 |
| 105.2 | 91.08 | 88.5 | time 30 | 11-11-2024 12:12:35 |
| 110.79 | 94.48 | 80.69 | time 30 | 11-11-2024 12:12:02 |
| 99.99 | 86.11 | 88.69 | time 30 | 11-11-2024 12:07:59 |
| 96.4 | 91.1 | 82.82 | time 30 | 11-11-2024 12:06:14 |
| 101.99 | 91.18 | 77.73 | time 30 | 11-11-2024 12:05:36 |
| 106.77 | 91.69 | 79.34 | time 30 | 11-11-2024 12:04:45 |
| 104.78 | 89.88 | 92.22 | time 30 | 11-11-2024 12:02:47 |
| 114.38 | 95.82 | 81.12 | time 30 | 11-11-2024 12:01:50 |
| 89.98 | 82.08 | 82.22 | time 30 | 11-11-2024 11:51:12 |


 --- 

### Top 10 results

| WPM | Accuracy | Consistency | Mode | Timestamp |
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


## Configuration

1. **Get API Key from account settings -> ape keys -> generate new key**
2. **Add generated api key to .env file variable apikey**
3. **Run get_data.py script that will load data from [Monkeytype](https://monkeytype.com/) and insert into sqllite3 db history.db (this wont be stored on your GitHub)**
4. **Error logs will be stored into logfile.log, and import status will be stored into import_status.log**
5. **stats.py script will get data from db and push them into GitHub account**
    
    