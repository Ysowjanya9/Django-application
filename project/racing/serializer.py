from rest_framework import serializers
from .models import Team, Driver, Race

class teamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class driverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

class raceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = '__all__'