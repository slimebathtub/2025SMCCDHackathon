from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from core.models import Center
from resources.forms import ItemForm
from resources.models import Item

from django.contrib.auth.decorators import login_required

# Create your views here.
def resources_view(request):
    return render(request, 'resources/sourcepage.html')

def center_item_list(reques):
    return

def sourcepage_view(request):
    items = Item.objects.all()
    
    # Apply search filters
    name = request.GET.get('name')
    if name:
        items = items.filter(name__icontains=name)

    tag_name = request.GET.get('tag')
    if tag_name:
        items = items.filter(tags__name=tag_name)

    loc_name = request.GET.get('location')
    if loc_name:
        items = items.filter(location__name=loc_name)

    if request.GET.get('available'):
        items = items.filter(status='available')

    if request.GET.get('unavailable'):
        items = items.filter(status='unavailable')

    from .models import Tag
    from core.models import Center
    tags = Tag.objects.all()
    locations = Center.objects.all()

    return render(request, 'resources/sourcepage.html', {
        'items': items,
        'tags': tags,
        'locations': locations,
        'request': request,
    })
