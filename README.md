
[Configuration](#configuration)
## My public Monkeytype [profile](https://monkeytype.com/profile/zp14)


        
## Typing History Stats (Last Updated: 17/11/2024 21:32)

| **Key Stats**               | **Overall Stats**       | **Last 10 Tests Stats**  |
|--------------------------|-------------------------|--------------------------|
| **Total Entries**        | 880           | 10                       |
| **Average WPM**          | 102.82           | 105.98    |
| **Average Accuracy**     | 90.87%          | 90.10%   |
| **Max WPM**              | 129.13               | 121.16        |
| **Min WPM**              | 64.77               | 87.17                        |
| **Total Duration**       | 07:21:06        | 00:05:00                        |


---
### Last 10 results

| WPM | Accuracy | Consistency | Mode | Date |
| --- | -------- | ----------- | ---- | --------- |
| 109.58 | 87.58 | 84.97 | time 30 | 17-11-2024 16:33:17 |
| 109.2 | 93.2 | 81.05 | time 30 | 17-11-2024 16:31:49 |
| 100.77 | 86.42 | 87.95 | time 30 | 17-11-2024 16:29:46 |
| 121.16 | 97.52 | 87.61 | time 30 | 15-11-2024 14:28:51 |
| 96.79 | 88.39 | 86.94 | time 30 | 15-11-2024 10:43:50 |
| 101.56 | 89.71 | 87.93 | time 30 | 15-11-2024 10:43:16 |
| 105.6 | 91.72 | 86.1 | time 30 | 15-11-2024 10:39:54 |
| 87.17 | 81.03 | 84.15 | time 30 | 15-11-2024 10:38:54 |
| 111.99 | 93.19 | 83.1 | time 30 | 15-11-2024 10:38:05 |
| 115.98 | 92.26 | 88.61 | time 30 | 15-11-2024 10:36:53 |


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

1. **Get API Key from account settings -> ape keys -> generate new key -> check active button next to apekey's name**
2. **Add generated api key to .env file variable apikey**
3. **(If you've got less than 1000 tests completed) Run get_data_max_1000.py script that will load data from [Monkeytype](https://monkeytype.com/) and insert into sqllite3 db history.db (this wont be stored on your GitHub)**
4. **Error logs will be stored into logfile.log, and import status will be stored into import_status.log**
5. **stats.py script will get data from db and push them into GitHub account**
6. **You can use API call via ApeKey 30 times per day, so after you reach this limit you wont get any answear and in logfile you will see *Problem with inserting data 0* row**
7. **incremental_import.py will check for the last result time in db and download just those tests that are younger than that. It will also update automatically into GitHub account unless you comment last 2 line of code.**

# UPDATE for 1000+ tests
    
**As monkeytype API enables just 1000 rows to be downloaded via API call, for proper inintial insertion to db tests where there are more than 1000 on your profile
you should export csv file from [Monkeytype account](https://monkeytype.com/account) (over results at the bottom of the site)
and put this csv file into project folder (or set proper path to this file into variable csv_file), then run inintial_csv_read.py script.**
    