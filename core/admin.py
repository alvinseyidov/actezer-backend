from django.contrib import admin
from .models import Country, City

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_code', 'created_at')
    search_fields = ('name', 'iso_code')
    ordering = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'latitude', 'longitude', 'created_at')
    search_fields = ('name', 'country__name')
    list_filter = ('country',)
    ordering = ('name',)
