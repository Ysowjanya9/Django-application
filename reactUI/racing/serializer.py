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
    # def update(self, instance, validated_data):
    #     if 'logo_image' not in validated_data:
    #         validated_data['logo_image'] = instance.logo_image
    #         return super().update(instance, validated_data)

class driverSerializer(serializers.ModelSerializer):
    team = serializers.SlugRelatedField(slug_field='team_name',required=False,allow_null=True,queryset = Team.objects.all())
    upcoming_races = serializers.SerializerMethodField()
    completed_races = serializers.SerializerMethodField()
    class Meta:
        model = Driver
        fields = ['id','first_name','last_name','date_of_birth','team','completed_races','upcoming_races']
    def get_upcoming_races(self,obj):
        return [race.track_name for race in obj.upcoming_races()]
    def get_completed_races(self,obj):
        return [race.track_name for race in obj.completed_races()]

class raceSerializer(serializers.ModelSerializer):
    driver = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all(), many=True, write_only=True)
    driver_names = serializers.SerializerMethodField()
    class Meta:
        model = Race
        fields = ['id', 'track_name', 'city', 'country', 'race_date', 'registration_closure_date', 'driver', 'driver_names']
    def get_driver_names(self, obj):
        return [f"{driver.first_name} {driver.last_name}" for driver in obj.driver.all()]
    def validate(self, data):
        race_date = data.get('race_date')
        registration_closure_date = data.get('registration_closure_date')
        if registration_closure_date and registration_closure_date >= race_date:
            raise serializers.ValidationError({'registration_closure_date': 'Must be before the race date.'})
        return data
