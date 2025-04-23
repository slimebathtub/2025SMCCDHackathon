from django import forms
from resources.models import Item
from rooms.models import Room

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
        fields = ['name', 'status', 'capacity', 'location']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'