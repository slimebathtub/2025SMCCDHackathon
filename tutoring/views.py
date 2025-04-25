from django.shortcuts import render
from .models import TutoringDailySchedule
from datetime import datetime
# Create your views here.

def tutoring_table(request):
    # 1) pull the user’s choice (default to first choice)
    today = datetime.now().strftime("%A")  # e.g. "Monday
    weekdays = [day[0] for day in TutoringDailySchedule.WEEKDAYS]
    
    subjects = TutoringDailySchedule.objects.values_list('subject', flat=True).distinct()
    
    if today in weekdays:
        default_day = today
    else:
        default_day = TutoringDailySchedule.WEEKDAYS[0][0]  
        
    #default_subject = "Math"    
    
    selected_day = request.GET.get("day", default_day)
    selected_subject = request.GET.get("subj", "")
    # base queryset: filter by day always
    qs = TutoringDailySchedule.objects.filter(weekday=selected_day)

    # only narrow by subject if one was chosen
    if selected_subject:
        qs = qs.filter(subject=selected_subject)

    context = {
        "weekdays":         TutoringDailySchedule.WEEKDAYS,
        "selected_day":     selected_day,
        "subjects":         subjects,
        "selected_subject": selected_subject,
        "sessions":         qs,
    }
    return render(request, "tutoring/tutoring_table.html", context)
    
    
    

    # 3) pass both the list of choices and the selected value
    context = {
        "weekdays":         TutoringDailySchedule.WEEKDAYS,   # list of (value,label)
        "selected_day":     selected_day,
        "selected_subject": selected_subject,
        "sessions":         sessions,
        "subjects":          subjects
    }
    return render(request, "tutoring/tutoring_table.html", context)

# superuser 
# name: edgar
# pw: 123any456