import pandas as pd
#import sqlite3

''' This script is meant to parse the MRC (Math Resource Center) tutoring schedule
    into a .db file that will be then displayed in the website
    
    The linear_search function is used to find the first occurrence of a key in a
    specific column or row. So that it can be adapted to other schedule formats as
    well. After that I just find the table limits by the "CLOSED" and "HOURS" keywords.
'''

MRC_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vRK33wM-yaF-svgS2vuzaSO_YP-Uh_NeZRP5MVRMIlp9tcOQIvcJRQLbpjhOyd0U73ou_IaW-l9G2Hm"
    "/pub?gid=105984831&single=true&output=csv"
)
WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
#pandas indexing: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html
# most crucial : #df.iloc[y1:y2, x1:x2] # y1:y2 = rows, x1:x2 = columns

SOURCE_DF = pd.read_csv(MRC_URL)

class DailySchedule:
    def __init__(self, courses = "General", time="00:00 AM - 00:00 PM", subject="Math", location="MRC", weekday="Sunday"):
        self.courses = courses
        self.time = time
        self.location = location
        self.subject = subject
        self.weekday = weekday

    def __repr__(self):
        return f'{self.subject} - {self.class_name} at {self.location}, {self.time}'



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


def clean(element):
    name = str(element).strip()
    if name.__contains__("Stats"):
        name = "Stats"
    elif name and name.strip() not in ["nan", "CLOSED"]:
        name = "General Math"
        
    return name

def format_df():
    global SOURCE_DF
    # 1. Find y1, y2, and x2, note x1 = 0
    y1 = linear_search("HOURS", start_index=0, axis="col")
    y2 = linear_search("CLOSED", start_index=3, axis="col")
    x2 = linear_search("CLOSED", start_index=y1+1, axis="row")
   
    # 2. Build and clean up header
    df = SOURCE_DF.iloc[y1:y2, 0:x2]    
    df = df.reset_index(drop=True) 
    df.columns = df.iloc[0].str.split().str[0]
    df = df.iloc[1:].reset_index(drop=True)

    # 3. Merge the first two columns and drop the second
    col1, col2 = df.columns[:2]
    df[col1] = df[col1].astype(str).str.cat(df[col2].astype(str), sep=" - ")
    df = df.drop(columns=col2)
    
    # 4. Combine every three rows by joining non‐null strings with “ | ”
    combined_rows = []
    for i in range(0, df.shape[0], 3):  # the excel has gaps of 3
        row1 = df.iloc[i + 0].tolist() if i + 0 < len(df) else []
        row2 = df.iloc[i + 1].tolist() if i + 1 < len(df) else []
        row3 = df.iloc[i + 2].tolist() if i + 2 < len(df) else []
        
        
        combined_row = [row1[0]]  # keep first column as is, dropping rows 2 & 3
        for j in range(1, df.shape[1]):
            triplet = set(map(clean,[row1[j], row2[j], row3[j]]))
            combined_row.append(
                " , ".join(
                    filter(lambda x: x and x != "nan", triplet)
                )
            )
        combined_rows.append(combined_row)
    df = pd.DataFrame(combined_rows, columns=df.columns)
    #print(df)
    
    return df
   
#weekday, subject, class_name, time, location
        
def create_weekdays_dfs(df = format_df()):
    """
    Split a schedule-DF whose first column is time and next five columns are
    Mon–Fri into five dfs:
      monday_df, tuesday_df, wednesday_df, thursday_df, friday_df

    Each output has exactly these columns, in order:
      subject, courses, time, location
    """
    # 1) Identify columns
    time_col = df.columns[0]
    day_cols = list(df.columns[1:6])  # [Mon, Tue, Wed, Thu, Fri]

    # 2) Build one DataFrame per day
    week_dfs = dict()
    week_index = 0
    for day in day_cols:
        # assemble a new DataFrame
        mask = (
            df[day].astype(str).str.strip().ne("CLOSED")  # != "CLOSED"
            & df[day].notna()                             # drop NaN
            & df[day].astype(str).str.strip().ne("")      # drop empty strings
        )
        clean_df = df.loc[mask]
        day_df = pd.DataFrame({
            "subject":  ["Math"] * len(clean_df),
            "courses":  clean_df[day].astype(str),
            "time":     clean_df[time_col].astype(str),
            "location": ["MRC"] * len(clean_df),
        })
        
        week_day = WEEK_DAYS[week_index]
        week_index += 1
        week_dfs[week_day] = day_df

    return week_dfs
    
    
def main():
    weekdays = create_weekdays_dfs()
    
    for day in weekdays:
        print(day)
        print(weekdays[day])
    
   
if __name__ == "__main__":
    main()
