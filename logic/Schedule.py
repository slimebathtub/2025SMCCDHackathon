import pandas as pd
import sqlite3
import os
import django
import yaml

try:
    from .TimeHandler import TimeRange 
except ImportError:
    from TimeHandler import TimeRange 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "campus_site.settings")
django.setup()

from tutoring.models import TutoringDailySchedule
from core.models import Center

center_info_path = os.path.join("tutoring", "databases", "centers_info.yaml")
with open(center_info_path, "r") as file:
    data = yaml.safe_load(file)

WEEK_DAYS, WEEK_DICT = data["WEEK_DAYS"], data["WEEK_DICT"]
COLUMNS, SUBJ_DICT = data["COLUMNS"], data["SUBJ_DICT"] 
URL_DICT, CENTERS_ID = data["URL_DICT"], data["CENTERS_ID"]  
INV_CENTERS_ID = {v["full_name"]: k for k, v in CENTERS_ID.items()}
INVALIDS = {"nan", "NAN", "", None}
#######################################################################################################################

class TeachingSlot:
    def __init__(self,
        day      : str      = "NAN",
        subject  : str      = "NAN",
        courses  : str      = "NAN",
        location : str      = "NAN",
        tutors   : str      = "NAN",
        time     : TimeRange = None
    ):
        self.day      = day
        self.subject  = subject
        self.courses  = courses
        self.location = location
        self.tutors   = tutors 
        self.time     = time
    @property
    def is_ok(self):
        return all(getattr(self, attr) not in INVALIDS for attr in vars(self))
    
    def as_dict(self):
        return {col: getattr(self, col) for col in COLUMNS}
        

        

class Schedule:
    _buffer : list[dict] = []
    _weekday_type = pd.CategoricalDtype(categories=WEEK_DAYS, ordered=True)
    def __init__(self, location: str = "Unknown"):
        self.location = location
        self.df = pd.DataFrame(columns=COLUMNS)

    def add_slot(self, ts: TeachingSlot):
        if ts.is_ok:
            self._buffer.append(ts.as_dict())
    
    def finalize_week(self):
        self.df = pd.DataFrame(self._buffer, columns=COLUMNS)
        self.df["day"] = self.df["day"].astype(self._weekday_type)
        self.df.sort_values(["day", "time"], inplace=True, ignore_index=True)
                
    def to_sql(self):
        path = os.path.join("tutoring", "databases", f"{self.location}.db")
        conn = sqlite3.connect(path)
        cur = conn.cursor()

        table_name = "schedule"
        # drop existing
        cur.execute(f'DROP TABLE IF EXISTS "{table_name}"')
        conn.commit()

        if self.df is None or self.df.empty:
            conn.close()
            return

        df_copy = self.df.copy()
        # normalize courses for storage
        df_copy["courses"] = df_copy["courses"].apply(
            lambda x: ", ".join(x) if isinstance(x, list) else str(x)
        )
        df_copy["time"] = df_copy["time"].apply(lambda x: str(x))

        # write single flat table
        df_copy.to_sql(table_name, conn, if_exists="append", index=False)
        conn.close()

        
    def to_instances(self) -> list[TutoringDailySchedule]:
        """
        Turn every row in the master DataFrame into unsaved TutoringDailySchedule instances.
        """
        instances = []
        center_id = INV_CENTERS_ID.get(self.location)
        center = Center.objects.get(center_id=center_id)

        if self.df is None or self.df.empty:
            return instances

        for _, row in self.df.iterrows():
            inst = TutoringDailySchedule(
                weekday=row["day"],
                subject=row["subject"],
                courses=row["courses"],  
                time=row["time"],
                tutors=row["tutors"],
                location=center,
            )
            instances.append(inst)
        return instances
