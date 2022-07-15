from django.forms import ModelForm
from cms.models import Marbar

class MarbarForm(ModelForm):
    class Meta:
        model = Marbar
        fields = ['date_start', 'duration', 'title']
