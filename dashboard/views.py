from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from resources.models import Item
from core.models import Center
from tutoring.models import TutoringDailySchedule
from .forms import ItemForm

def dashboard_view(request):
    items = Item.objects.all()
    tutor_schedules = TutoringDailySchedule.objects.all()
    return render(request, 'dashboard/dashboard.html', {
        'items': items,
        'tutor_session': tutor_schedules,
    })

def item_edit_form(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204)  # 告訴前端成功了，不用回傳畫面
        else:
            return render(request, 'dashboard/item_edit_form.html', {'form': form})
    else:
        form = ItemForm(instance=item)
        return render(request, 'dashboard/item_edit_form.html', {'form': form})