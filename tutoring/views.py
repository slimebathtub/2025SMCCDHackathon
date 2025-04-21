from django.shortcuts import render
from .models import TutoringDailySchedule
from datetime import datetime
# Create your views here.

def tutoring_table(request):
    # 1) pull the user’s choice (default to first choice)
    today = datetime.now().strftime("%A")  # e.g. "Monday
    weekdays = [day[0] for day in TutoringDailySchedule.WEEKDAYS]
    if today in weekdays:
        default_day = today
    else:
        default_day = TutoringDailySchedule.WEEKDAYS[0][0]  
        
    selected_day = request.GET.get("day", default_day)
    # 2) fetch that day’s sessions
    sessions = (
        TutoringDailySchedule.objects
        .filter(weekday=selected_day)
    )

    # 3) pass both the list of choices and the selected value
    context = {
        "weekdays":     TutoringDailySchedule.WEEKDAYS,   # list of (value,label)
        "selected_day": selected_day,
        "sessions":     sessions,
    }
    return render(request, "tutoring/tutoring_table.html", context)

# superuser 
# name: edgar
# pw: 123any456