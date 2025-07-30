import pandas as pd
import re
from Schedule import LC_URL, WEEK_DAYS, SUBJ_DICT, Schedule, TeachingSlot
import sqlite3

SOURCE_DF = pd.read_csv(LC_URL, dtype=str)
LOCATION = "Learning Center"

# columns are subject, courses, time, location, tutors
# df.iloc[Monday , 9:00]  returns the courses
lc = Schedule(LOCATION)
    
def LC_extract_info():
    global SOURCE_DF  
    df = SOURCE_DF.iloc[2:19, 0:6].reset_index(drop=True)
    df.columns = ["Subject"] + WEEK_DAYS

    for _, row in df.iterrows():
        for day in WEEK_DAYS:
            # "Accounting\n\n100,121,131"
            ts = TeachingSlot(location=LOCATION, day=day)
             
            try:
                subj_name, courses_str = str(row.get("Subject")).split("\n\n", 1)
                subj_name, courses_str = map(str.strip, [subj_name, courses_str])
                tutors_str = row.get(day)
                courses = ", ".join([c.strip() for c in courses_str.split(',') if c.strip()])
            except ValueError as e:
                print(f"Oops, something wrong in row {row}")
                raise e
            
            if pd.isna(tutors_str) or not str(tutors_str).strip() or not courses:
                continue   
            
            ts.subject = subj_name
            ts.courses = courses

            # Gideon: 4 pm - 6:30 pm\nACTG 100\nACTG 121
            for tutor_block in tutors_str.split("\n\n", 1):
                lines = tutor_block.strip().split('\n')
                
                # first line format is "TutorName: time‑range"
                if not tutor_block.strip() or ":" not in lines[0]:
                    continue              
                
                tutor, time_str = lines[0].split(":", 1)
                ts.tutor = tutor.strip()
                
                times = [c.strip() for c in re.split(r",|/", time_str) if c.strip()]
                for time in times:
                    ts.time = time
                    lc.add_slot(ts)
                    
            lc.finalize_day(day)
    lc.fix_time()
    

def save_sqlite(day, df):
    
    if "courses" in df.columns:
        df = df.copy()
        df["courses"] = df["courses"].apply(
            lambda x: ", ".join(x) if isinstance(x, list) else str(x)
        )
    
    conn = sqlite3.connect("lc_database.db")
    df.to_sql(day, conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()

def main():
    LC_extract_info()
    for day in WEEK_DAYS:
        #print(day)
        #print(lc.week_dfs.get(day))
        save_sqlite(day, lc.week_dfs.get(day))
   
   
if __name__ == "__main__":
    main()   