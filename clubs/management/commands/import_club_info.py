# clubs/management/commands/import_schedule.py
from django.core.management.base import BaseCommand
from clubs.models import ClubInfo
from logic.ClubsParser import clubs_parser
from logic.TimeHandler import time_handler as th
import pandas as pd

objs = []
WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

class Command(BaseCommand):
    help = "Import the MRC schedule into TutoringDailySchedule, one row per session."

    def handle(self, *args, **options):
        # clear out old data
        ClubInfo.objects.all().delete()
       
        # this is a dictionary, where a weekday is mapped into a DataFrame
        # e.g. weeek_dfs["Monday"] = whatever schedule we have for Monday
        df = clubs_parser()   
        records = df.to_dict(orient="records")      
        objs = [ClubInfo(**rec) for rec in records]
    
        # bulk‐create them
        ClubInfo.objects.bulk_create(objs)
        self.stdout.write(self.style.SUCCESS(
            f"Imported {len(objs)} clubs across."
        ))
