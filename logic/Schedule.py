import pandas as pd
import os
import sqlite3
from tutoring.models import TutoringDailySchedule
try:
    from .TimeHandler import merge_time_ranges as mtr
except ImportError:
    from TimeHandler import merge_time_ranges as mtr
    
    
WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
COLUMNS = ["subject", "courses", "time", "location", "tutors"]
WEEK_DICT = dict(zip(["MON", "TUES", "WED", "THURS", "FRI"], WEEK_DAYS))

SUBJ_DICT = {
    "Biology"          : "BIOL",
    "Chemistry"        : "CHEM",
    "Computer Science" : "CIS",
    "Engineering"      : "ENGR",
    "Math"             : "MATH",
    "Physics"          : "PHYS",
    "Accounting"       : "ACC",
    "Business"         : "BUSS",
    "Economics"        : "ECON"
}

LC_URL = (
    "https://docs.google.com/spreadsheets/u/1/d/e/"
    "2PACX-1vSCej3JQkmwsCFHSLs1VYQQJ9KjtmFCeAaWKxRjsRlD6nawQJDKqycveJzAzqXHVC0u5NYl8SIfyHgQ"
    "/pub?gid=0&single=true&output=csv"
)
ISC_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vTXGQcyHvjXs4o_4sFErW432K2jNC_kiSc6HN2ynw4kUufv1dYSLMsRORsG1GyMhpY_H89YohQegFYq"
    "/pub?gid=0&single=true&output=csv"
)
MRC_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vRK33wM-yaF-svgS2vuzaSO_YP-Uh_NeZRP5MVRMIlp9tcOQIvcJRQLbpjhOyd0U73ou_IaW-l9G2Hm"
    "/pub?gid=105984831&single=true&output=csv"
)

# df columns are WEEK_DAYS
# df rows are the time

class TeachingSlot:
    def __init__(
        self,
        location : str = "NAN",
        day      : str = "NAN",
        subject  : str = "NAN",
        courses  : str = "NAN",
        tutors    : str = "NAN",
        time     : str = "NAN"
    ):
        self.location = location
        self.subject  = subject
        self.courses  = courses
        self.time     = time
        self.day      = day
        self.tutors    = tutors  
        
    def is_ok(self):
        invalids = {"nan", "NAN", "", None}
        return all(getattr(self, attr) not in invalids for attr in vars(self))

        

class Schedule:
    _day_buffers = {day: [] for day in WEEK_DAYS}
    
    def __init__(self, location: str = "Unknown"):
        self.location = location
        self.week_dfs = {day: pd.DataFrame(columns=COLUMNS) for day in WEEK_DAYS}

    def add_slot(self, ts: TeachingSlot):
        if ts.day not in self._day_buffers:
            print(f"Day '{ts.day}' is not recognized. Slot not added.")
            return

        if not ts.is_ok():
            return

        new_entry = {
            "subject"  : ts.subject,
            "courses"  : ts.courses,
            "time"     : ts.time,
            "location" : ts.location,
            "tutors"   : ts.tutors
        }

        self._day_buffers[ts.day].append(new_entry)
        
    def finalize_day(self, day):
        self.week_dfs[day] = pd.DataFrame(self._day_buffers[day], columns=COLUMNS)
    
    def finalize_week(self):
        for day in WEEK_DAYS:
            self.finalize_day(day)
        
    def fix_time(self):
        for day in WEEK_DAYS:
            self.week_dfs[day] = mtr(self.week_dfs[day])
            #WEEK_DAYS[day] = WEEK_DAYS[day].reset_index(drop=True)
        
    def to_sql(self):
        path = os.path.join("tutoring", "databases", self.location + ".db")
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        for day in WEEK_DAYS:
            df = self.week_dfs.get(day)
            # Pre-process your DataFrame as before…
            if df is None or df.empty:
                return
            
            df["courses"] = df["courses"].apply(
                    lambda x: ", ".join(x) if isinstance(x, list) else str(x)
                ) 
           
            # <-- drop the table first if it exists
            cur.execute(f'DROP TABLE IF EXISTS "{day}"')
            conn.commit()

            # now append (or replace) will never fail on CREATE
            df.to_sql(day, conn, if_exists='append', index=False)

        conn.close()
        
    def to_instances(self) -> list[TutoringDailySchedule]:
        """
        Turn every row in every weekday-DataFrame into a
        TutoringDailySchedule (unsaved) instance.
        """
        instances = []
        for day, df in self.week_dfs.items():
            if df is None or df.empty:
                continue
            for _, row in df.iterrows():
                # row['courses'] is already a Python list (or string)
                inst = TutoringDailySchedule(
                    weekday = day,
                    subject = row['subject'],
                    courses = row['courses'],      # JSONField can take list
                    time = row['time'],
                    tutors = row['tutors'],
                    location = row['location']
                )
                instances.append(inst)
        return instances