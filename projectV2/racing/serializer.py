from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Team, Driver, Race

class teamSerializer(serializers.ModelSerializer):
    drivers = serializers.SerializerMethodField()
    class Meta:
        model = Team
        fields = ['id','team_name','city','country','drivers','logo_image','description']
    def get_drivers(self, obj):
        return [f"{driver.first_name} {driver.last_name}" for driver in obj.drivers.all()]


class driverSerializer(serializers.ModelSerializer):
    team = serializers.SlugRelatedField(slug_field='team_name',required=False,allow_null=True,queryset = Team.objects.all())
    races = serializers.SlugRelatedField(slug_field='track_name',queryset = Race.objects.all(),many=True)
    class Meta:
        model = Driver
        fields = ['id','first_name','last_name','date_of_birth','team','races']


class raceSerializer(serializers.ModelSerializer):
    driver = serializers.SlugRelatedField(slug_field='first_name',required=False,allow_null=True,queryset = Driver.objects.all(),many=True)
    class Meta:
        model = Race
        fields = ['id','track_name','city','country','race_date','registration_closure_date','driver']
    def validate(self, data):
         race_date=data.get('race_date')
         registration_closure_date=data.get('registration_closure_date')
         if registration_closure_date and registration_closure_date>=race_date:
           raise ValidationError({'registration_closure_date': 'Must be before the race date.'})
         return data