# tutoring/management/commands/import_schedule.py
from django.core.management.base import BaseCommand
from django.db import transaction
from tutoring.models import TutoringDailySchedule
from logic.MRCParser import parse_mrc
from logic.LCParser import parse_lc
from logic.ISCParser import parse_isc
from logic.Schedule import WEEK_DAYS
from datetime import datetime


def order_key(inst):
    # 01:00 PM
    weekday_order = WEEK_DAYS.index(inst.weekday)  
    start_time =  datetime.strptime(inst.time.split(" - ")[0], "%I:%M %p")
    return (weekday_order, start_time)

class Command(BaseCommand):
    help = "Import the MRC, ISC and LC schedules into TutoringDailySchedule, one row per session."

    def handle(self, *args, **options):
        # clear out old data
        TutoringDailySchedule.objects.all().delete()
       
        # this is a dictionary, where a weekday is mapped into a DataFrame
        # e.g. weeek_dfs["Monday"] = whatever schedule we have for Monday
        
        schedules = [parse_mrc(), parse_isc(), parse_lc()]
        objs = []
        for sched in schedules:
            objs.extend(sched.to_instances())
        objs.sort(key=order_key)
        
        # Bulk insert inside a transaction
        with transaction.atomic():
            TutoringDailySchedule.objects.bulk_create(objs, batch_size=500)

        self.stdout.write(self.style.SUCCESS(
            f"Imported {len(objs)} tutoring slots."
        ))
      
