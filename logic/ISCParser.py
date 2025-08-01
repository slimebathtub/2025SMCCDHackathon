import pandas as pd
import re

try:
    from .Schedule import ISC_URL, WEEK_DAYS, WEEK_DICT, SUBJ_DICT, Schedule, TeachingSlot
except ImportError:
    from Schedule import ISC_URL, WEEK_DAYS, WEEK_DICT, SUBJ_DICT, Schedule, TeachingSlot


SOURCE_DF = pd.read_csv(ISC_URL)
LOCATION = "Integrated Science Center"

def clean(subject, courses):
    cleaned_courses = []
    subject = str(subject).strip()
    
    try:
        match = re.search(r'\d+', courses)
        if "all" in courses.lower():
            courses = f'(Any)'
        if "up to" in courses.lower():
            if match:
                upper_bound = match.group()
                courses = f'up to {upper_bound}'
            else:
                courses = f'(Any)'
                
        
        courses_list = courses.split(",")
        subj = SUBJ_DICT.get(subject)
        
        cleaned_courses = [f'{course.strip()}' for course in courses_list if course.strip()]
        
        return subject, ", ".join(cleaned_courses)
    
    except AttributeError as e:
        print(f"Error processing courses: {e}")
        print(f"Original courses string: {courses}")
        print(f"Subject: {subject}")
        raise e
        
    
# df.iloc[y1:y2, x1:x2] # y1:y2 = row range, x1:x2 = column range
isc = Schedule(location=LOCATION)

def parse_isc():
    global SOURCE_DF
    ts = TeachingSlot(location=LOCATION)
    #subject, courses, time, day, tutors
    
    df = SOURCE_DF.iloc[0:-2].reset_index(drop=True)   
    df.columns = ["day", "time", "tutor", "classes"]
    for i, row in df.iterrows():
        if row["day"] in SUBJ_DICT:
            ts.subject = row.iloc[0] # same as row[day] but i want to emphasize is not a day
            continue #skip next row bc are just headers
        
        day_key = str(row["day"]).split(',')[0].strip()
        
        if day_key not in WEEK_DICT:
            continue
        
        ts.day = WEEK_DICT[day_key]
        
        try:
            ts.time, ts.courses = clean(row.iloc[1], row.iloc[3]) 
            ts.tutors = row.iloc[2]
        except TypeError as e:
            print(f"Error processing row {i}: {e}")
            print("Subject and courses:", ts.subject, ts.courses)
            raise e
        except:
            print(f"Damn, something wrong on row {i}: {row}")
            continue
        
        isc.add_slot(ts)
    isc.finalize_week()
    isc.fix_time()
    return isc
    

def main():
    global isc
    parse_isc()
    isc.to_sql()
    


if __name__ == "__main__":
    main()
  
    
