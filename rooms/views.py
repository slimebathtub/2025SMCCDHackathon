from django.shortcuts import render

from core.models import Center
from rooms.models import Room

# Create your views here.
def room_list_view(request):
    
    # all_locations = Room.objects.values_list('location', flat=True).exclude(location__isnull=True).distinct()
    all_capacities = Room.objects.values_list('capacity', flat=True).exclude(capacity__isnull=True).distinct().order_by('capacity')
    
    rooms = Room.objects.all()

    all_locations = Center.objects.all()
    
    capacity = request.GET.get('capacity')
    if capacity and capacity.isdigit():
        rooms = rooms.filter(capacity__gte=int(capacity))
    
    if request.GET.get('available'):
        rooms = rooms.filter(status='available')

    if request.GET.get('unavailable'):
        rooms = rooms.filter(status='unavailable')

    return render(request, 'rooms/roompage.html', {
        'rooms': rooms,
        'locations': all_locations,
        'capacities': all_capacities
    })