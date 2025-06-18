from django import forms
from django.core.exceptions import ValidationError
from .models import Team, Driver, Race

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = '__all__'
    
class RaceForm(forms.ModelForm):
    class Meta:
        model = Race
        fields = '__all__'

    
    