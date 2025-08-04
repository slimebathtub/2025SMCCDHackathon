import pandas as pd
try:
    from .Schedule import URL_DICT, WEEK_DAYS, Schedule, TeachingSlot
    from .TimeHandler import TimeRange
except ImportError:
    from Schedule import URL_DICT, WEEK_DAYS, Schedule, TeachingSlot
    from TimeHandler import TimeRange


''' This script is meant to parse the MRC (Math Resource Center) tutoring schedule
    into a .db file that will be then displayed in the website
    
    The linear_search function is used to find the first occurrence of a key in a
    specific column or row. So that it can be adapted to other schedule formats as
    well. After that I just find the table limits by the "CLOSED" and "HOURS" keywords.
'''

# df.iloc[y1:y2, x1:x2] # y1:y2 = rows, x1:x2 = columns
SOURCE_DF = pd.read_csv(URL_DICT.get("MRC"))
LOCATION = "Math Resource Center"

def linear_search(key="CLOSED", start_index=0, axis="col"):
    global SOURCE_DF
    
    if axis not in ["row", "col"]:
        raise ValueError("type must be 'row' or 'col'")
    
    local_df = SOURCE_DF.T.copy() if axis == "row" else SOURCE_DF.copy()
    
    arr = local_df.iloc[:, start_index].astype(str) 
    mask = arr.str.contains(key, case=False, na=False) 
    first_pos = next((pos for pos, hit in enumerate(mask) if hit), None)
    
    return first_pos

# relevant table : (finds w gonna find)
# (0,y1) - (x2,y1) 
# (0,y2) - (x2,y2) 
# for example, Friday might finish earlier than other weekdays, so we need to check for that

def clean(names):
    stats_found = any("(Stats)" in str(name) for name in names)
    course = "Any" if stats_found else "General"
    tutors = ", ".join(
        str(name).replace("(Stats)", "") for name in names 
        if name and "nan" not in str(name)
    )
        
    return tutors, course
            
def format_df():
    global SOURCE_DF
    # 1. Find y1, y2, and x2, note that x1 = 0
    y1 = linear_search("HOURS", start_index=0, axis="col")
    y2 = linear_search("CLOSED", start_index=3, axis="col")
    x2 = linear_search("CLOSED", start_index=y1+1, axis="row")
   
    # 2. Build and clean up header
    df = SOURCE_DF.iloc[y1:y2, 0:x2].reset_index(drop=True)
    df.columns = df.iloc[0].str.split().str[0]
    df = df.iloc[1:].reset_index(drop=True)

    # 3. Merge the first two columns and drop the second
    col1, col2 = df.columns[:2]
    df[col1] = df[col1].astype(str).str.cat(df[col2].astype(str), sep=" - ")
    df = df.drop(columns=col2)
    
    # 4. Combine every three rows by joining non‐null strings
    combined_rows = []
    for i in range(0, df.shape[0], 3):  # the excel has gaps of 3
        row1 = df.iloc[i + 0].tolist() if i + 0 < len(df) else []
        row2 = df.iloc[i + 1].tolist() if i + 1 < len(df) else []
        row3 = df.iloc[i + 2].tolist() if i + 2 < len(df) else []
        
        combined_row = [row1[0]]  # keep first column as is, dropping rows 2 & 3
        for j in range(1, df.shape[1]):
            triplet = clean([row1[j], row2[j], row3[j]])
            combined_row.append(triplet)
        combined_rows.append(combined_row)
    
    return pd.DataFrame(combined_rows, columns=df.columns)
   
#weekday, subject, class_name, time, location
mrc = Schedule(LOCATION)   

def parse_mrc():
    global SOURCE_DF
    df = format_df()
    ts = TeachingSlot(location=LOCATION, subject="Math", courses="General")
    
    for day in WEEK_DAYS:
        ts.day = day
        for _, row in df.iterrows():
            if day not in row or "HOURS" not in row:
                continue
            
            ts.time = TimeRange.from_string(row["HOURS"]) 
            ts.tutors, ts.courses = row[day]
            
            mrc.add_slot(ts)
    mrc.finalize_week()
    return mrc
    
def main():
    global mrc
    parse_mrc()
    mrc.to_sql()
    
if __name__ == "__main__":
    main()
