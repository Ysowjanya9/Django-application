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

    def clean(self):
       cleaned_data = super().clean()
       first_name = cleaned_data.get('first_name')
       last_name = cleaned_data.get('last_name')
       team = cleaned_data.get('team')
       if Driver.objects.filter(first_name=first_name, last_name=last_name, team=team).exclude(id=self.instance.id).exists():
           raise ValidationError(f"A driver named {first_name} {last_name} is already assigned to {team.team_name}.")
       return cleaned_data
    

class RaceForm(forms.ModelForm):
    class Meta:
        model = Race
        fields = '__all__'

    
    