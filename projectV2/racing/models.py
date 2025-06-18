from django.db import models
from datetime import date
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

def check_logo_size(img):
    max = 50 * 1024
    if  img.size > max:
        raise ValidationError("Logo size must be less than or equal to 50KB.")

class Team(models.Model):
    team_name = models.CharField(max_length=256,unique=True)
    city = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    logo_image = models.ImageField(upload_to='TeamLogos', validators=[check_logo_size])
    description = models.TextField(max_length=1024, blank=True)
    def __str__(self):
        return self.team_name
    
class Driver(models.Model):
    first_name = models.CharField(max_length=96)
    last_name = models.CharField(max_length=96)
    date_of_birth = models.DateField(validators=[MaxValueValidator(limit_value=date(2000,12,31))])
    team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='drivers',null=True,blank=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=['first_name','last_name'], name='unique_driver_name')]
    def completed_races(self):
        return self.races.filter(race_date__lt=date.today())
    def upcoming_races(self):
        return self.races.filter(race_date__gte=date.today())
    def __str__(self):
        return self.first_name + " " + self.last_name
     
class Race(models.Model):
   track_name = models.CharField(max_length=256, unique=True)
   city = models.CharField(max_length=18)
   country = models.CharField(max_length=18)
   race_date = models.DateField(validators=[MinValueValidator(limit_value=date.today())])
   registration_closure_date = models.DateField(null=True, blank=True)
   driver = models.ManyToManyField(Driver, blank=True, related_name='races')
   def clean(self):
       if self.registration_closure_date and self.registration_closure_date>=self.race_date:
           raise ValidationError({'registration_closure_date': 'Must be before the race date.'})
   def __str__(self):
        return self.track_name  
   

