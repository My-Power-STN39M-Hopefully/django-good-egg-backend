from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views
from .views import UserList, UserDetail, RegistrationAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # # users
    path('', views.UserList.as_view(), name='user_list'),
    path('<int:pk>', views.UserDetail.as_view(), name='user_detail'),
    path('register', RegistrationAPIView.as_view()),
    # user authentication
    path('signin/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('signin/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
