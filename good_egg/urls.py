from django.urls import path
from . import views
from . import models

# Create your urls here.
urlpatterns = [
    path('', views.landing_page, name='landing_page'),

]
