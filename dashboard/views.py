from django import apps
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from resources.models import Item, Tag
from core.models import Center
from rooms.models import Room
from tutoring.models import TutoringDailySchedule
from .forms import ItemForm, RoomForm
from django.apps import apps

CENTERS = ["MRC", "ISC", "LC"]

@login_required
def dashboard_view(request):
    print("DEBUG request.path =", request.path)
    user = request.user
    if not user.is_authenticated:
        # you could redirect to login or treat as “else” below
        items = Item.objects.none()
        tutor_schedules = TutoringDailySchedule.objects.none()

    if user.username in CENTERS:
        items = Item.objects.filter(location__name=user.username)
        tutor_schedules = TutoringDailySchedule.objects.filter(location=user.username)
    
    return render(request, 'dashboard/pages/resources_page.html', {
        'items': items,
        'tutor_session': tutor_schedules,
        'username': user.username
    })

def item_edit_form(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            # If user create a new teg
            new_tag_str = form.cleaned_data.get('new_tags', "")
            if new_tag_str:
                tag_names = []
                name_sep = new_tag_str.split(',')
                for name in name_sep:
                    cleaned = name.strip()
                    if cleaned:
                        tag_names.append(cleaned)

                for name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=name)
                    item.tags.add(tag)

            return HttpResponse(status=204)
        else:
            return render(request, 'dashboard/forms/item_edit_form.html', {'form': form})
    else:
        form = ItemForm(instance=item)
        return render(request, 'dashboard/forms/item_edit_form.html', {'form': form})

@csrf_exempt
def item_create_form(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            # If user create a new teg
            new_tag_str = form.cleaned_data.get('new_tags', "")
            if new_tag_str:
                tag_names = []
                for name in new_tag_str.split(','):
                    cleaned = name.strip()
                    if cleaned:
                        tag_names.append(cleaned)
                for name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=name)
                    item.tags.add(tag)
            return HttpResponse(status=204)
        else:
            return render(request, 'dashboard/forms/item_edit_form.html', {'form': form})
    else:
        form = ItemForm()
        return render(request, 'dashboard/forms/item_edit_form.html', {'form': form})

@csrf_exempt
def generic_delete_view(request, model_name, pk):
    Model = apps.get_model('rooms' if model_name == 'room' else 'resources', model_name.capitalize())
    obj = get_object_or_404(Model, id=pk)
    
    if request.method == 'POST':
        obj.delete()
        return HttpResponse(status=204)
    
    return HttpResponse(status=405)

@login_required
def dashboard_room_view(request):
    print("DEBUG request.path =", request.path)
    rooms = Room.objects.all()
    tutor_schedules = TutoringDailySchedule.objects.all()
    return render(request, 'dashboard/pages/room_page.html', {
        'rooms': rooms,
    })

@csrf_exempt
def room_edit_form(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204)
        else:
            return render(request, 'dashboard/forms/room_edit_form.html', {'form': form})
    else:
        form = RoomForm(instance=room)
        return render(request, 'dashboard/forms/room_edit_form.html', {'form': form})


@csrf_exempt
def room_create_form(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204)
        else:
            return render(request, 'dashboard/forms/room_edit_form.html', {'form': form})
    else:
        form = RoomForm()
        return render(request, 'dashboard/forms/room_edit_form.html', {'form': form})

