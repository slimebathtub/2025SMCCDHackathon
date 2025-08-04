# tutoring/management/commands/import_schedule.py
from django.core.management.base import BaseCommand
from django.db import transaction
from tutoring.models import TutoringDailySchedule
from logic.MRCParser import parse_mrc
from logic.LCParser import parse_lc
from logic.ISCParser import parse_isc


class Command(BaseCommand):
    help = "Import the MRC, ISC and LC schedules into TutoringDailySchedule, one row per session."

    def handle(self, *args, **options):
        # clear out old data
        TutoringDailySchedule.objects.all().delete()
        
        schedules = [parse_mrc(), parse_isc(), parse_lc()]
        objs = []
        for sched in schedules:
            objs.extend(sched.to_instances())
        #objs.sort(key=order_key)
        
        # Bulk insert inside a transaction
        with transaction.atomic():
            TutoringDailySchedule.objects.bulk_create(objs, batch_size=500)

        self.stdout.write(self.style.SUCCESS(
            f"Imported {len(objs)} tutoring slots."
        ))
      
