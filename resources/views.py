from django.shortcuts import get_object_or_404, redirect, render

from core.models import Center
from resources.forms import ItemForm
from resources.models import Item

from django.contrib.auth.decorators import login_required

# Create your views here.
def resources_view(request):
    return render(request, 'resources/sourcepage.html')

@login_required
def center_item_list(request):
    center = Center.objects.get(user=request.user)
    items = Item.objects.filter(location=center)
    return render(request, 'resources/itemlist.html', {'items': items})

@login_required
def update_item(request, item_id):
    center = Center.objects.get(user=request.user)
    item = get_object_or_404(Item, id=item_id, location=center)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('resources:itemlist')
    else:
        form = ItemForm(instance=item)
    return render(request, 'resources/updateitem.html', {'form': form})