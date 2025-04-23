import pandas as pd
import re
from .TimeHandler import time_handler as th
# ISC URL
ISC_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vTXGQcyHvjXs4o_4sFErW432K2jNC_kiSc6HN2ynw4kUufv1dYSLMsRORsG1GyMhpY_H89YohQegFYq"
    "/pub?gid=0&single=true&output=csv"
)

WEEK_DICT = {
    "MON"   : "Monday",
    "TUES"  : "Tuesday",
    "WED"   : "Wednesday",
    "THURS" : "Thursday",
    "FRI"   : "Friday",
}

SUBJ_DICT = {
    "Biology"  : "BIOL",
    "Chemistry": "CHEM",
    "Computer Science" : "CIS",
    "Engineering" : "ENGR",
    "Math" : "MATH",
    "Physics" : "PHYS",
}

WEEK_DAYS = [v for v in WEEK_DICT.values()]
SOURCE_DF = pd.read_csv(ISC_URL)


def clean(subject, courses, location):
    cleaned_courses = []
    subject = str(subject).strip()
    
    try:
        match = re.search(r'\d+', courses)
        if "all" in courses.lower():
            courses = f'(Any)'
        if "up to" in courses.lower():
            if match:
                upper_bound = match.group()
                courses = f'(up to {upper_bound})'
            else:
                courses = f'(Any)'
                
        
        courses_list = courses.split(",")
        subj = SUBJ_DICT[subject]
        
        cleaned_courses = [f'{subj} {course.strip()}' for course in courses_list if course.strip()]
        
        return subject, cleaned_courses, location
    
    except AttributeError as e:
        print(f"Error processing courses: {e}")
        print(f"Original courses string: {courses}")
        print(f"Subject: {subject}")
        raise e
        
    
    



# df.iloc[y1:y2, x1:x2] # y1:y2 = row range, x1:x2 = column range
# Build one DataFrame per day,
# columns are : subject, courses, time, location
def ISC_create_weekday_dfs():
    global SOURCE_DF
    
    df = SOURCE_DF.iloc[1:-2].reset_index(drop=True)   
    week_records = {day: [] for day in WEEK_DAYS}
    week_dfs = {day: pd.DataFrame(
        columns=["subject", "courses", "time", "location"])
        for day in WEEK_DAYS
    } 
    
    subj = ""
    
    for i, row in df.iterrows():
        if row.iloc[0] in SUBJ_DICT:
            subj = row.iloc[0]
            continue #skip next row bc are just headers
        
        if row.iloc[0] not in WEEK_DICT.keys():
            continue
        
        day = WEEK_DICT[row.iloc[0]]
        records = week_records[day]
        try:
            time = row.iloc[1]
            tutor = row.iloc[2]
            courses = row.iloc[3]
        except:
            print(f"Damn, something wrong on row {i}: {row}")
            continue
        
        
        try:
            subj, courses, location = clean(subj, courses, "ISC")
        except TypeError as e:
            print(f"Error processing row {i}: {e}")
            print("LHS:",subj, courses, "ISC")
            print("RHS:",clean(subj, courses, "ISC"))
            raise e
        
        records.append({
            "subject": subj,
            "courses": courses,
            "time": time,
            "location": location,
        })
            
    for day in WEEK_DAYS:
        week_dfs[day] = th(pd.DataFrame.from_records(
            week_records[day], columns=["subject", "courses", "time", "location"]
        ))
    
    return week_dfs
    

def main():
    week_dfs = ISC_create_weekday_dfs()
    for day, df in week_dfs.items():
        print(f"DataFrame for {day}:")
        print(df)  
        print("\n")

# Load ISC data and save it as an Excel file
def download_isc_schedule():
    isc_df = pd.read_csv(ISC_URL)  # Load the ISC data from the URL
    isc_df.to_excel("ISC_Schedule.xlsx", index=False)  # Save it as an Excel file
    print("ISC schedule downloaded as 'ISC_Schedule.xlsx'.")


# Example usage
if __name__ == "__main__":
    main()
    #download_isc_schedule()
    
