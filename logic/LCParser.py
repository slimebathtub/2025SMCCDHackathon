import pandas as pd
import re
from .TimeHandler import time_handler as th

LC_URL = (
    "https://docs.google.com/spreadsheets/u/1/d/e/"
    "2PACX-1vSCej3JQkmwsCFHSLs1VYQQJ9KjtmFCeAaWKxRjsRlD6nawQJDKqycveJzAzqXHVC0u5NYl8SIfyHgQ"
    "/pub?gid=0&single=true&output=csv"
)
WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
SOURCE_DF = pd.read_csv(LC_URL)

def clean(courses):
    cleaned_courses = []
    
    for course in courses:
        if not course or pd.isna(course) or "appointment" in course.lower():
            continue
        if "all" in course.lower() and "stats" in course.lower():
            course = ["General Math", "Stats"]
        elif "all" in course.lower():
            course = f'{course.split()[0]} (Any)'
            
        cleaned_courses.append(course)
    return cleaned_courses
    
# relevant table : 
# (0, 2) - ( 6, 2) 
# (0,19) - ( 6,19)

def LC_create_weekday_dfs():
    global SOURCE_DF
    
    df = SOURCE_DF.iloc[2:19, 0:6]
    df = df.reset_index(drop=True) 
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)

    
    # Build one DataFrame per day,
    # columns are : subject, courses, time, location
    week_dfs = dict()
    
    for day in WEEK_DAYS:
        records = []
        for _, row in df.iterrows():
            # "Accounting\n\n100,121,131" 
            subj_parts = str(row["Subject"]).split("\n\n")
            subj_name = subj_parts[0].strip()

            cell = row.get(day)
            if pd.isna(cell) or not str(cell).strip():
                continue

            # Gideon: 4 pm - 6:30 pm\nACTG 100\nACTG 121
            tutor_blocks = str(cell).split("\n\n")
            for tutor_block in tutor_blocks:
                tutor_block = tutor_block.strip()
                if not tutor_block:
                    continue

                lines = tutor_block.split("\n")
                # first line format is "TutorName: time‑range"
                if ":" not in lines[0]:
                    continue
                tutor_name, time_str = lines[0].split(":", 1)
                tutor_name = tutor_name.strip()
                time_arr = [c.strip() for c in re.split(r",|/", time_str) if c.strip()]
                # the rest of the lines are courses
                course_list = [c.strip() for c in lines[1:] if c.strip()]
                for i, course in enumerate(course_list):
                    if "BLDG" in course:
                        location, course_list[i] = 'B2 at 240/250', f'General {subj_name}'
                    else:
                        location = "Learning Center"
                
                course_list = clean(course_list)
                if not course_list:
                    continue
                        
                for time in time_arr:
                    records.append({
                        "subject" : subj_name,
                        "courses" : course_list,
                        "time"    : time,
                        "location": location,
                    })

        # build a DataFrame for this weekday
        week_dfs[day] = pd.DataFrame.from_records(
            records,
            columns=["subject", "courses", "time", "location"]
        )
        # unify time_format
        week_dfs[day] = th(week_dfs[day])
        week_dfs[day] = week_dfs[day].reset_index(drop=True)
    return week_dfs


def main():
    weekdays = LC_create_weekday_dfs()
    
    for day in weekdays:
        print(day)
        print(weekdays[day])
   
if __name__ == "__main__":
    main()
   