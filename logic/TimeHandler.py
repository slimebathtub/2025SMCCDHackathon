import re
import pandas as pd
from datetime import datetime

def merge_time_ranges(df: pd.DataFrame):
    
    df = time_handler(df)
    merged_rows = []
    current_row = ''
    
    if df.empty:
        return
    current_row = df.iloc[0].copy()
    
    
    for i in range(1, len(df)):
        next_row = df.iloc[i]
        curr_start_t, curr_end_t = current_row["time"].split(" - ")
        next_start_t, next_end_t = next_row["time"].split(" - ")
        # unites identical consecutive rows (with adjacent time ranges)
        if (
            current_row["subject"] == next_row["subject"]
            and current_row["courses"] == next_row["courses"]
            and current_row["location"] == next_row["location"]
            and current_row["tutors"] == next_row["tutors"]
            and curr_end_t == next_start_t
        ):
            # Merge the time ranges
            current_row["time"] = f"{curr_start_t} - {next_end_t}"
        else:
            # Append the current row to the merged list and move to the next row
            merged_rows.append(current_row)
            current_row = next_row.copy()

    # Append the last row
    merged_rows.append(current_row)

    # Convert the merged rows back into a DataFrame
    merged_df = pd.DataFrame(merged_rows)
    return merged_df
    

def change_time_format(time_range):
    time = str(time_range).strip()
    # this time you are not escaping the pattern
    pattern = r'(\d{1,2})(:\d{2})?\s*(am|pm|AM|PM)?'
    
    #  thanks re, for existing
    start, end = re.split(r"\s*-\s*", time, 1)
    
    # Match and format the start time
    start_match = re.match(pattern, start.strip())
    start_formatted = format_time(start_match, default_period="PM") 
    
    # Match and format the end time
    end_match = re.match(pattern, end.strip())
    end_formatted = format_time(end_match)  
    
    return f"{start_formatted} - {end_formatted}"

def format_time(match, default_period=None):
    if not match:
        return ""
    hour, minutes, period = match.groups()
    hour = int(hour)
    if not minutes:
        minutes = ":00"   # Default to ":00" if minutes are missing
    if not period and default_period:  # If AM/PM is missing, use the default
        period = default_period
    if 7 <= hour <= 11:
        period = "AM" # this is ur fault MATH 145
    return f"{hour:02d}{minutes} {period.upper() if period else ''}"           
    
def time_handler(df : pd.DataFrame):
    df["time"] = df["time"].apply(change_time_format)
    
    df["start_time"] = df["time"].apply(
        lambda t: datetime.strptime(t.split(" - ")[0], "%I:%M %p")
    )
    df = df.sort_values(by="start_time")
    df = df.drop(columns=["start_time"])
    
    return df

def main():
    df = pd.DataFrame({
        "subject": ["Math", "Physics"],
        "courses": [["MATH 251", "MATH 253"], ["PHYS 100"]],
        "time": ["9am - 10:00 am", "11:00 am -11:30pm"],
        "location": ["MRC", "Learning Center"],
        "tutors" : ["Hey", "You!"]
    })
    df = time_handler(df)
    print(df["time"])
    
    
    
    
if __name__ == "__main__":
    main()