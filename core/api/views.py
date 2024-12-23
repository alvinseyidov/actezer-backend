from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.generics import UpdateAPIView, ListAPIView, CreateAPIView, RetrieveAPIView
from .serializers import *
from core.models import *


class CountryListView(ListAPIView):
    serializer_class = CountryListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Country.objects.all()


class CityListView(ListAPIView):
    serializer_class = CountryListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        country_id = self.request.query_params.get('country_id')
        if country_id:
            return City.objects.filter(country_id=country_id)
        return City.objects.all()


