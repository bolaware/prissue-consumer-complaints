from django.forms import ModelForm
from models import Feed
#from djnago import forms

class FeedForm(ModelForm):
    class Meta:
        model=Feed
        fields=('text','auth','files')
        
#class LikeForm(forms.Form):
