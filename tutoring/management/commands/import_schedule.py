# tutoring/management/commands/import_schedule.py
from django.core.management.base import BaseCommand
from tutoring.models import TutoringDailySchedule
from logic.MRCParser import MRC_create_weekday_dfs
from logic.LCParser import LC_create_weekday_dfs

objs = []
def check(week_dfs):
    global objs
    for day, df in week_dfs.items():
            # ensure columns are in the right order:
            df = df[["subject", "courses", "time", "location"]]
            for row in df.to_dict(orient="records"):
                # we'll need the day as an atribute for filtering
                row["weekday"] = day
                objs.append(TutoringDailySchedule(**row))

class Command(BaseCommand):
    help = "Import the MRC schedule into TutoringDailySchedule, one row per session."

    def handle(self, *args, **options):
        # clear out old data
        TutoringDailySchedule.objects.all().delete()
       
        # this is a dictionary, where a weekday is mapped into a DataFrame
        # e.g. weeek_dfs["Monday"] = whatever schedule we have for Monday
        mrc_week_dfs = MRC_create_weekday_dfs()
        lc_week_dfs = LC_create_weekday_dfs()
            
        # new instances
        check(mrc_week_dfs)
        check(lc_week_dfs)
    
        # bulk‐create them
        TutoringDailySchedule.objects.bulk_create(objs)
        self.stdout.write(self.style.SUCCESS(
            f"Imported {len(objs)} tutoring sessions across {len(mrc_week_dfs)} days."
        ))
