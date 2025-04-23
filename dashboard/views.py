from django.shortcuts import render

from resources.models import Item
from core.models import Center
from tutoring.models import TutoringDailySchedule

def dashboard_view(request):
    items = Item.objects.all()
    tutor_schedules = TutoringDailySchedule.objects.all()
    return render(request, 'dashboard/dashboard.html', {
        'items': items,
        'tutor_session': tutor_schedules,
    })