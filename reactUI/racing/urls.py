from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    
   # Team
   path('racing/teams/', views.team_list, name='team_list'),
   path('racing/teams/create/', views.team_create, name='team_create'),
   path('racing/teams/edit/<int:pk>/', views.team_edit, name='team_edit'),
   path('racing/teams/delete/<int:pk>/', views.team_delete, name='team_delete'),
   # Driver
   path('racing/drivers/', views.driver_list, name='driver_list'),
   path('racing/drivers/create/', views.driver_create, name='driver_create'),
   path('racing/drivers/edit/<int:pk>/', views.driver_edit, name='driver_edit'),
   path('racing/drivers/delete/<int:pk>/', views.driver_delete, name='driver_delete'),
   # Race
   path('racing/races/', views.race_list, name='race_list'),
   path('racing/races/create/', views.race_create, name='race_create'),
   path('racing/races/edit/<int:pk>/', views.race_edit, name='race_edit'),
   path('racing/races/delete/<int:pk>/', views.race_delete, name='race_delete'),

   # Team API
   path('racing/api/teams/create/', views.team_create_api.as_view()), # POST
   path('racing/api/teams/', views.team_list_api.as_view()), # GET
   path('racing/api/teams/edit/<int:pk>/', views.team_edit_api.as_view()), # GET, PUT, PATCH
   path('racing/api/teams/delete/<int:pk>/', views.team_delete_api.as_view()), # DELETE
   # Driver API
   path('racing/api/drivers/create/', views.driver_create_api.as_view()), # POST
   path('racing/api/drivers/', views.driver_list_api.as_view()), # GET
   path('racing/api/drivers/edit/<int:pk>/', views.driver_edit_api.as_view()), # GET, PUT, PATCH
   path('racing/api/drivers/delete/<int:pk>/', views.driver_delete_api.as_view()), # DELETE
   # Race API
   path('racing/api/races/create/',views.race_create_api.as_view()), # POST
   path('racing/api/races/',views.race_list_api.as_view()), # GET
   path('racing/api/races/edit/<int:pk>/',views.race_edit_api.as_view()), # GET, PUT, PATCH
   path('racing/api/races/delete/<int:pk>/',views.race_delete_api.as_view()), # DELETE
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 