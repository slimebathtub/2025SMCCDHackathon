from django.shortcuts import render
from .models import TutoringDailySchedule
# Create your views here.

def tutoring_table(request):
    # 1) pull the user’s choice (default to first choice)
    default_day = TutoringDailySchedule.WEEKDAYS[0][0]  # e.g. "Monday"
    selected_day = request.GET.get("day", default_day)
    

    # 2) fetch that day’s sessions
    sessions = (
        TutoringDailySchedule.objects
        .filter(weekday=selected_day)
        .order_by("time")
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