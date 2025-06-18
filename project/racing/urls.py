from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    # Team URLs
   path('teams/', views.team_list, name='team_list'),
   path('teams/create/', views.team_create, name='team_create'),
   path('teams/<int:pk>/edit/', views.team_update, name='team_edit'),
   path('teams/<int:pk>/delete/', views.team_delete, name='team_delete'),
   # Driver URLs
   path('drivers/', views.driver_list, name='driver_list'),
   path('drivers/create/', views.driver_create, name='driver_create'),
   path('drivers/<int:pk>/edit/', views.driver_update, name='driver_edit'),
   path('drivers/<int:pk>/delete/', views.driver_delete, name='driver_delete'),
   # Race URLs
   path('races/', views.race_list, name='race_list'),
   path('races/create/', views.race_create, name='race_create'),
   path('races/<int:pk>/edit/', views.race_update, name='race_edit'),
   path('races/<int:pk>/delete/', views.race_delete, name='race_delete'),
   #API
   path('TeamCreate/',views.TeamCreate.as_view()),
   path('TeamList/',views.TeamList.as_view()),
   path('TeamUpdate/<int:pk>/',views.TeamUpdate.as_view()),
   path('TeamDelete/<int:pk>/',views.TeamDelete.as_view()),
   path('DriverCreate/',views.DriverCreate.as_view()),
   path('DriverList/',views.DriverList.as_view()),
   path('DriverUpdate/<int:pk>/',views.DriverUpdate.as_view()),
   path('DriverDelete/<int:pk>/',views.DriverDelete.as_view()),
   path('RaceCreate/',views.RaceCreate.as_view()),
   path('RaceList/',views.RaceList.as_view()),
   path('RaceUpdate/<int:pk>/',views.RaceUpdate.as_view()),
   path('RaceDelete/<int:pk>/',views.RaceDelete.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)