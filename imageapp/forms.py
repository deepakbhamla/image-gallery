from django import forms
from .models import Tag
class GalleryForm(forms.Form):
    image = forms.FileField(
            label=False, 
            widget=forms.ClearableFileInput(attrs={'multiple': True,'id':'file-input','type':'file'}))

    tags = forms.ModelMultipleChoiceField(
            queryset=Tag.objects.all(),
            widget=forms.CheckboxSelectMultiple(attrs={'type':'checkbox'}))        
            
