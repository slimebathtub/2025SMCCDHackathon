from django.shortcuts import render
from .models import ClubInfo
# Create your views here.

def clubs_table(request):
    
    sessions = (
        ClubInfo.objects.all()
    )
    
    context = {
        "sessions":  sessions,
    }
    
    return render(request, "clubs/clubs_table.html", context)

# def clubs_table_edit(request):