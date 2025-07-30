from django import forms
from resources.models import Item, Tag
from rooms.models import Room
from core.models import Center

class ItemForm(forms.ModelForm):
    new_tags = forms.CharField(
        label='New Tags',
        required=False,
        help_text='Enter new tags (separated by commas)',
        widget=forms.TextInput(attrs={'placeholder': 'Enter new tags'})
    )
    class Meta:
        model = Item
        fields = ['name', 'status', 'tags', 'location']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'status', 'capacity']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'location' in self.fields:
            self.fields['location'].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class CenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = ['center_full_name', 'center_short_name', 'center_building_address']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'location' in self.fields:
            self.fields['location'].disabled = True

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter tag name'
        })
