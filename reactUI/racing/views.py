from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import generics
from rest_framework.response import Response
from .serializer import teamSerializer, driverSerializer, raceSerializer
from .models import Team, Driver, Race
from .forms import TeamForm, DriverForm, RaceForm

def home(request):
    return render(request, 'home.html')

def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('team_list')
    else:
        form = TeamForm()
    return render(request, 'teams/team_form.html',{'form':form, 'heading': 'Create a Team'})

def team_list(request):
    teams = Team.objects.all()
    return render(request, 'teams/team_list.html',{'teams': teams})

def team_edit(request, pk):
    try:
        team = Team.objects.get(id=pk)
    except Team.DoesNotExist:
        messages.error(request, "Team not found.")
        return redirect('team_list')
    if request.method =='POST':
        form = TeamForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            return redirect('team_list')
    else:
        form=TeamForm(instance=team)
    return render(request, 'teams/team_form.html',{'form':form, 'heading': 'Update a Team'})

def team_delete(request, pk):
   try:
       team = Team.objects.get(id=pk)
   except Team.DoesNotExist:
       messages.error(request, "Team not found.")
       return redirect('team_list')
   if team.drivers.filter(races__isnull=False).exists():
       messages.error(request, "Cannot delete team with registered drivers in races.")
       return redirect('team_list')
   team.delete()
   messages.success(request, "Team deleted successfully.")
   return redirect('team_list')

def driver_create(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('driver_list')
    else:
        form = DriverForm()
    return render(request, 'drivers/driver_form.html',{'form':form, 'heading': 'Create a Driver'})

def driver_list(request):
    drivers = Driver.objects.all()
    return render(request, 'drivers/driver_list.html',{'drivers': drivers})

def driver_edit(request, pk):
    try:
        driver = Driver.objects.get(id=pk)
    except Driver.DoesNotExist:
        return redirect('driver_list')
    if request.method =='POST':
        form = DriverForm(request.POST, instance=driver)
        if form.is_valid():
            form.save()
            return redirect('driver_list')
    else:
        form = DriverForm(instance=driver)
    return render(request, 'drivers/driver_form.html',{'form':form, 'heading': 'Update a Driver'})

def driver_delete(request, pk):
   try:
       driver = Driver.objects.get(id=pk)
   except Driver.DoesNotExist:
       messages.error(request, "Driver not found.")
       return redirect('driver_list')
   if driver.races.exists():
       messages.error(request, "Cannot delete driver with registered in races.")
       return redirect('driver_list')
   driver.delete()
   messages.success(request, "Driver deleted successfully.")
   return redirect('driver_list')

def race_create(request):
    form = RaceForm()
    if request.method == 'POST':
        form = RaceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('race_list')
    return render(request, 'races/race_form.html',{'form':form, 'heading': 'Create a Race'})

def race_list(request):
    races = Race.objects.all()
    return render(request, 'races/race_list.html',{'races': races})

def race_edit(request, pk):
    try:
        race = Race.objects.get(id=pk)
    except Race.DoesNotExist:
        return redirect('race_list')
    form = RaceForm(instance=race)
    if request.method =='POST':
        form = RaceForm(request.POST, instance=race)
        if form.is_valid():
            form.save()
            return redirect('race_list')
    return render(request, 'races/race_form.html',{'form':form, 'heading': 'Update a Race'})

def race_delete(request, pk):
   try:
       race = Race.objects.get(id=pk)
   except Race.DoesNotExist:
       messages.error(request, "Race not found.")
       return redirect('race_list')
   if race.driver.exists():
       messages.error(request, "Cannot delete race with registered drivers.")
       return redirect('race_list')
   race.delete()
   messages.success(request, "Race deleted successfully.")
   return redirect('race_list')


class team_create_api(generics.CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = teamSerializer

class team_list_api(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = teamSerializer

class team_edit_api(generics.RetrieveUpdateAPIView):
    queryset = Team.objects.all()
    serializer_class = teamSerializer

class team_delete_api(generics.DestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = teamSerializer
    def delete(self, request, *args, **kwargs):
       team = self.get_object()
       if team.drivers.filter(races__isnull=False).exists():
           return Response({"message": "Cannot delete team with drivers in races."})
       team.delete()
       return Response({"message": "Team deleted successfully."})

class driver_create_api(generics.CreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = driverSerializer

class driver_list_api(generics.ListAPIView):
    queryset = Driver.objects.all()
    serializer_class = driverSerializer

class driver_edit_api(generics.RetrieveUpdateAPIView):
    queryset = Driver.objects.all()
    serializer_class = driverSerializer

class driver_delete_api(generics.DestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = driverSerializer
    def delete(self, request, *args, **kwargs):
       driver = self.get_object()
       if driver.races.exists():
           return Response({"message": "Cannot delete driver registered in races."})
       driver.delete()
       return Response({"message": "Driver deleted successfully."})
    
class race_create_api(generics.CreateAPIView):
    queryset = Race.objects.all()
    serializer_class = raceSerializer

class race_list_api(generics.ListAPIView):
    queryset = Race.objects.all()
    serializer_class = raceSerializer

class race_edit_api(generics.RetrieveUpdateAPIView):
    queryset = Race.objects.all()
    serializer_class = raceSerializer

class race_delete_api(generics.DestroyAPIView):
    queryset = Race.objects.all()
    serializer = raceSerializer
    def delete(self, request, *args, **kwargs):
       race = self.get_object()
       if race.driver.exists():
           return Response({"message": "Cannot delete race with registered drivers."})
       race.delete()
       return Response({"message": "Race deleted successfully."})