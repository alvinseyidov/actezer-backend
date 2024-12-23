from rest_framework import serializers
from rest_framework.authtoken.models import Token
from core.models import *



class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"

class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"