from django.contrib import admin
from .models import Activity, ActivityParticipant, ActivityComment, ActivityChatMessage

from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin  # ✅ Use GIS Admin
from django.contrib.gis import forms
from activity.models import Activity


@admin.register(Activity)
class ActivityAdmin(OSMGeoAdmin):
    list_display = ('name', 'category', 'start_datetime', 'city', 'people_limit', 'status', 'created_by')
    search_fields = ('name', 'category__name', 'city__name')
    list_filter = ('city', 'status', 'category')
    ordering = ('start_datetime',)

    # ✅ Correct way to add a map widget
    formfield_overrides = {
        'activity_location': {'widget': forms.OSMWidget(attrs={'default_lon': 0, 'default_lat': 0, 'default_zoom': 12})},
        'activity_meeting_location': {'widget': forms.OSMWidget(attrs={'default_lon': 0, 'default_lat': 0, 'default_zoom': 12})},
    }

@admin.register(ActivityParticipant)
class ActivityParticipantAdmin(admin.ModelAdmin):
    list_display = ('activity', 'user', 'joined_at')
    search_fields = ('activity__name', 'user__username')


@admin.register(ActivityComment)
class ActivityCommentAdmin(admin.ModelAdmin):
    list_display = ('activity', 'user', 'content', 'created_at')
    search_fields = ('activity__name', 'user__username', 'content')


@admin.register(ActivityChatMessage)
class ActivityChatMessageAdmin(admin.ModelAdmin):
    list_display = ('activity', 'user', 'content', 'created_at')
    search_fields = ('activity__name', 'user__username', 'content')
