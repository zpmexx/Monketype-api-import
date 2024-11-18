import matplotlib.pyplot as plt
import pandas as pd 
import sqlite3
import os
def create_and_export_charts():
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()


    db_data = cursor.execute("""SELECT 
        STRFTIME('%d-%m-%Y', timestamp / 1000, 'unixepoch') AS date, 
        AVG(wpm) AS avg_wpm
    FROM typing_history
    GROUP BY date
    ORDER BY timestamp;
    """).fetchall()


    dates = [item[0] for item in db_data] 
    wpm = [item[1] for item in db_data]  

    wpm_series = pd.Series(wpm)
    rolling_mean = wpm_series.rolling(window=10, min_periods=1).mean()  # Adjust window size as needed

    plt.figure(figsize=(12, 6))
    plt.plot(dates, wpm, marker='o', linestyle='-', alpha=0.4, label='Original WPM', color='gray')  # Raw data
    plt.plot(dates, rolling_mean, linestyle='-', color='blue', label='Trend (Rolling Avg)', linewidth=2)  # Trendline

    plt.title("Typing Speed Trend Over Time", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Words Per Minute (WPM)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.xticks(dates[::5], rotation=45)  # Show fewer date labels
    plt.tight_layout()
    
    typing_speed_file = "typing_speed_trend.png"

# Delete the old file if it exists
    if os.path.exists(typing_speed_file):
        os.remove(typing_speed_file)
    

    plt.savefig("typing_speed_trend.png", format='png')

    cursor.execute("SELECT MAX(wpm) FROM typing_history")
    max_wpm = cursor.fetchone()[0]


    range_width = 10
    import math
    # Calculate the number of ranges needed
    num_ranges = math.ceil(max_wpm / range_width)


    case_statement = "CASE "

    for i in range(num_ranges):
        lower_bound = i * range_width - .50
        lower_bound = 0 if lower_bound < 0 else lower_bound
        upper_bound = (i + 1) * range_width - 0.51
        case_statement += f"""WHEN wpm >= {lower_bound} AND wpm <= {upper_bound}
        THEN '{int(lower_bound+1)}-{int(upper_bound)}' """
        
    case_statement += "END AS wpm_range"
    db_data = cursor.execute(f"""
    SELECT {case_statement}, COUNT(*) AS count
    FROM typing_history
    GROUP BY wpm_range
    ORDER BY wpm_range;
    """).fetchall()

    sorted_data = sorted(db_data, key=lambda x: int(x[0].split('-')[0]))

    lowest_bound = sorted_data[0][0].split('-')[0]

    for i in range(0, int(lowest_bound), 10):
        upper_bound = i + 9
        # Insert each range at the beginning of the sorted data
        sorted_data.insert(0, (f"{i}-{upper_bound}", 0))
    sorted_data = sorted(sorted_data, key=lambda x: int(x[0].split('-')[0]))

    ranges = [range[0] for range in sorted_data]
    counts = [range[1] for range in sorted_data]

# Create the bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(ranges, counts, color='skyblue')

    # Add the count values on top of the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 2, str(int(yval)), 
                ha='center', va='bottom', fontsize=10, color='black')

    # Adding labels and title
    plt.title('WPM Ranges and Their Counts', fontsize=16)
    plt.xlabel('WPM Range', fontsize=12)
    plt.ylabel('Count', fontsize=12)

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)

    # Display the chart
    plt.tight_layout()
    
    count_tests_chart_file = "count_tests.png"

# Delete the old file if it exists
    if os.path.exists(count_tests_chart_file):
        os.remove(count_tests_chart_file)
    
    plt.savefig("count_tests.png", format='png')

if __name__ == "__main__":
    create_and_export_charts()