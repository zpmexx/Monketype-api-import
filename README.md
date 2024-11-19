
[Configuration](#configuration)
## My public Monkeytype [profile](https://monkeytype.com/profile/zp14)


        
## Typing History Stats (Last Updated: 19/11/2024 17:14)

| **Key Stats**               | **Overall Stats**       | **Last 10 Tests Stats**  |
|--------------------------|-------------------------|--------------------------|
| **Total Entries**        | 900           | 10                       |
| **Average WPM**          | 102.98           | 108.27    |
| **Average Accuracy**     | 90.92%          | 92.34%   |
| **Max WPM**              | 129.13               | 120.8        |
| **Min WPM**              | 64.77               | 95.2                        |
| **Total Duration**       | 07:31:07        | 00:05:00                        |


---

### Last 10 results

| | WPM | Accuracy | Consistency | Mode | Date |
| --- | --- | -------- | ----------- | ---- | --------- |
| 1 | 98.0 | 91.95 | 86.76 | time 30 | 19-11-2024 16:07:13 |
| 2 | 95.2 | 87.38 | 86.24 | time 30 | 19-11-2024 16:06:37 |
| 3 | 111.98 | 91.62 | 91.1 | time 30 | 19-11-2024 16:01:54 |
| 4 | 109.97 | 92.04 | 88.77 | time 30 | 19-11-2024 15:55:35 |
| 5 | 112.39 | 94.89 | 81.87 | time 30 | 19-11-2024 15:53:19 |
| 6 | 111.15 | 90.34 | 83.79 | time 30 | 19-11-2024 15:51:51 |
| 7 | 120.8 | 97.8 | 84.29 | time 30 | 18-11-2024 16:06:09 |
| 8 | 104.4 | 91.08 | 85.05 | time 30 | 18-11-2024 16:05:29 |
| 9 | 106.39 | 90.58 | 84.51 | time 30 | 18-11-2024 16:04:13 |
| 10 | 112.38 | 95.67 | 81.56 | time 30 | 18-11-2024 16:03:39 |


 --- 

### Top 10 results

| | WPM | Accuracy | Consistency | Mode | Date |
| --- | --- | -------- | ----------- | ---- | --------- |
| 1 | 129.13 | 97.93 | 87.46 | time 30 | 20-07-2024 16:54:21 |
| 2 | 126.37 | 99.08 | 86.0 | time 30 | 05-08-2024 14:25:56 |
| 3 | 125.96 | 95.82 | 86.11 | time 30 | 09-08-2024 12:56:13 |
| 4 | 125.55 | 98.18 | 85.59 | time 30 | 09-10-2024 16:32:56 |
| 5 | 124.8 | 98.12 | 86.59 | time 30 | 18-11-2024 15:57:37 |
| 6 | 124.78 | 99.06 | 87.92 | time 30 | 02-11-2024 18:46:45 |
| 7 | 123.56 | 97.56 | 87.97 | time 30 | 16-08-2024 16:52:42 |
| 8 | 123.15 | 96.98 | 84.75 | time 30 | 28-06-2024 17:01:24 |
| 9 | 123.14 | 96.95 | 86.04 | time 30 | 20-08-2024 17:01:55 |
| 10 | 122.79 | 94.38 | 87.25 | time 30 | 25-07-2024 13:09:46 |


 --- 


        
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
    