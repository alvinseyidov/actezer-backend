from django.conf.urls import include
from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'core-api'

urlpatterns = [
    path('country/list/', CountryListView.as_view(), name="country-list"),
    path('city/list/', CityListView.as_view(), name="city-list"),
]