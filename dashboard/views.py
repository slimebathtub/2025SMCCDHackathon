import json
from django.contrib import messages
#from xxlimited import new
from django import apps
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password

from resources.models import Item, Tag
from core.models import Center
from rooms.models import Room
# from tutoring.models import TutoringDailySchedule
from .forms import ItemForm, RoomForm, CenterForm, TagForm
from django.apps import apps

CENTERS = ["MRC", "ISC", "LC"]


@login_required
def dashboard_view(request):
    print("DEBUG request.path =", request.path)
    user = request.user
    if not user.is_authenticated:
        # you could redirect to login or treat as “else” below
        items = Item.objects.none()
        # tutor_schedules = TutoringDailySchedule.objects.none()
    elif user.username in CENTERS:
        items = Item.objects.filter(location__user__username=user.username)
        # tutor_schedules = TutoringDailySchedule.objects.filter(location__user_name=user.username)
    else:
        items = Item.objects.all()
    
    #filter:
    filter_status = request.GET.get('filter', 'all')
    if filter_status == 'unavailable':
        items = items.filter(status='unavailable')
    return render(request, 'dashboard/pages/resources_page.html', {
        'items': items,
        # 'tutor_session': tutor_schedules,
        'username': user.username,
        'filter_status': filter_status,
    })

def item_edit_form(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    center = Center.objects.get(user=request.user)
    item.location = center

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
            item = form.save(commit=False)
            center = Center.objects.get(user=request.user)
            item.location = center
            item.save()
            # If user create a new tag
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
def generic_delete_view(request, model_name, id):
    Model = apps.get_model('rooms' if model_name == 'room' else 'resources', model_name.capitalize())
    obj = get_object_or_404(Model, id=id)

    if request.method == 'POST':
        obj.delete()
        return HttpResponse(status=204)
    
    return HttpResponse(status=405)

@login_required
def dashboard_room_view(request):
    rooms = Room.objects.filter(location__user__username=request.user.username)
    # tutor_schedules = TutoringDailySchedule.objects.all()
    
    #filter:
    filter_status = request.GET.get('filter', 'all')
    if filter_status == 'unavailable':
        rooms = rooms.filter(status='unavailable')
    return render(request, 'dashboard/pages/room_page.html', {
        'rooms': rooms,
        'filter_status': filter_status,
    })

@csrf_exempt
def room_edit_form(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    center = Center.objects.get(user=request.user)
    room.location = center

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            room.save()
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
            room = form.save(commit=False)
            center = Center.objects.get(user=request.user)
            room.location = center
            room.save()
            return HttpResponse(status=204)
        else:
            return render(request, 'dashboard/forms/room_edit_form.html', {'form': form})
    else:
        form = RoomForm()
        return render(request, 'dashboard/forms/room_edit_form.html', {'form': form})


def dashboard_setting_view(request):
    center = get_object_or_404(Center, user=request.user)
    if request.method == 'POST':
        center.center_full_name = request.POST.get("center_fullname", center.center_full_name)
        center.center_short_name = request.POST.get("shortcut", center.center_short_name)
        center.center_building_address = request.POST.get("address", center.center_building_address)
        center.save()
        messages.success(request, 'Settings updated successfully.')
    
        user = center.user
        new_username = request.POST.get("user_fullname")
        new_password = request.POST.get("password")

        # Update password if provided
        if new_password:
            if check_password(new_password, user.password):
                messages.error(request, 'Password cannot be the same as the old one.')
            else:
                user.set_password(new_password)

        if new_username:
            user.username = new_username
        
        user.save()
        
        return redirect('setting_page')

    form = CenterForm(instance=center)
    return render(request, 'dashboard/pages/setting_page.html', {
        'form': form,
        'center': center,
    })

def Tag_management_setting(request):
    return render(request, 'dashboard/pages/tag_manage_page.html',{
        'tags': Tag.objects.all(),
    })

@csrf_exempt 
def bulk_delete_tags(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tag_ids = data.get('ids', [])
            Tag.objects.filter(id__in=tag_ids).delete()
            return JsonResponse({'status': 'success', 'deleted': tag_ids})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)


def tag_edit_view(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            updated_tag = form.save(commit=False)
            updated_tag.location = Center.objects.get(user=request.user)  # 確保 location 不被竄改
            updated_tag.save()
            return HttpResponse(status=204)
    else:
        form = TagForm(instance=tag)
    return render(request, 'dashboard/forms/tag_edit_form.html', {'form': form})


def tag_create_view(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.location = Center.objects.get(user=request.user)
            tag.save()
            return HttpResponse(status=204)
    else:
        form = TagForm()
    return render(request, 'dashboard/forms/tag_edit_form.html', {'form': form})