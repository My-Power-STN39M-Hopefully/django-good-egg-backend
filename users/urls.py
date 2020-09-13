from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views
from .views import UserList, UserDetail, RegistrationAPIView
from allauth.account.views import confirm_email
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # # users
    path('', views.UserList.as_view(), name='user_list'),
    path('<int:pk>', views.UserDetail.as_view(), name='user_detail'),
    path('register', RegistrationAPIView.as_view()),
    # user authentication
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^account/', include('allauth.urls')),
    url(r'^accounts-rest/registration/account-confirm-email/(?P<key>.+)/$',
        confirm_email, name='account_confirm_email')
]
