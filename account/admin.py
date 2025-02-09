from django.contrib import admin
from .models import CustomUser, UserImage, Interest, UserRating

from django.contrib.gis.db import models
from django.contrib.gis.forms.widgets import OSMWidget
from django.contrib.gis import admin
from django.contrib.gis.db import models
from django.contrib.gis.forms.widgets import OSMWidget
from account.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'country', 'city', 'birthday', 'activity_radius', 'map_location_display')
    search_fields = ('username', 'email', 'country__name', 'city__name')
    list_filter = ('country', 'city')
    ordering = ('username',)
    formfield_overrides = {
        models.PointField: {"widget": OSMWidget(attrs={"map_srid": 4326, "map_width": 800, "map_height": 500})},
    }

    def map_location_display(self, obj):
        """ Show Latitude and Longitude in Admin List View """
        if obj.map_location_point:
            return f"({obj.map_location_point.y}, {obj.map_location_point.x})"
        return "No Location"

    map_location_display.short_description = "Map Location (Lat, Long)"


@admin.register(UserImage)
class UserImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'image', 'uploaded_at')
    search_fields = ('user__username',)
    list_filter = ('uploaded_at',)
    ordering = ('-uploaded_at',)


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)



@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = ('rated_user', 'rated_by', 'rating', 'created_at')
    search_fields = ('rated_user__username', 'rated_by__username')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)