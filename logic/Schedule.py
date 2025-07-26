import pandas as pd

WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
COLUMNS = ["subject", "courses", "time", "location", "tutors"]
from .TimeHandler import time_handler as th

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
        tutor    : str = "NAN",
        time     : str = "NAN"
    ):
        self.location = location
        self.subject  = subject
        self.courses  = courses
        self.time     = time
        self.day      = day
        self.tutor    = tutor  

class Schedule:
    _day_buffers = {day: [] for day in WEEK_DAYS}
    
    def __init__(self, location: str = "Unknown"):
        self.location = location
        self.week_dfs = {day: pd.DataFrame(columns=COLUMNS) for day in WEEK_DAYS}

    def add_slot(self, ts: TeachingSlot):
        if ts.day not in self._day_buffers:
            print(f"Day '{ts.day}' is not recognized. Slot not added.")
            return

        new_entry = {
            "subject"  : ts.subject,
            "courses"  : ts.courses,
            "time"     : ts.time,
            "location" : ts.location,
            "tutors"   : ts.tutor
        }

        self._day_buffers[ts.day].append(new_entry)
        
    def finalize_day(self, day):
        self.week_dfs[day] = pd.DataFrame(self._day_buffers[day], columns=COLUMNS)
        
    def fix_time(self):
        for day in WEEK_DAYS:
            self.week_dfs[day] = th(self.week_dfs[day])
            #WEEK_DAYS[day] = WEEK_DAYS[day].reset_index(drop=True)

        