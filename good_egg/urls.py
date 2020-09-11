from rest_framework.routers import DefaultRouter
from .models import Force
from django.urls import path, include
from . import views
from . import models


# Create your urls here.
urlpatterns = [
    path('', views.landing_page, name='landing_page'),

    # force
    path('force/', views.ForceList.as_view(), name='force_list'),
    path('force/<int:pk>', views.ForceDetail.as_view(), name='force_detail'),

    # officer
    path('officers/', views.OfficerList.as_view(), name='officer_list'),
    path('officer/<int:pk>', views.OfficerDetail.as_view(), name='officer_detail'),
    path('officers/apples-and-eggs', views.GoodEggsBadApples.as_view(),
         name='good_eggs_bad_apples'),

    # incident
    path('incident/', views.IncidentList.as_view(), name='incident_list'),
    path('incident/<int:pk>', views.IncidentDetail.as_view(), name='incident_detail'),
    path('incident/recent', views.RecentIncidents.as_view(), name='incident_recent')

]
