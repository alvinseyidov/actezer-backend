from django.contrib import admin
from .models import Activity, ActivityParticipant, ActivityComment, ActivityChatMessage

from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin  # ✅ Use GIS Admin
from activity.models import Activity


@admin.register(Activity)
class ActivityAdmin(OSMGeoAdmin):  # ✅ Enables Map for PointField
    list_display = ('name', 'category', 'start_datetime', 'city', 'people_limit', 'status', 'created_by')
    search_fields = ('name', 'category__name', 'city__name')
    list_filter = ('city', 'status', 'category')
    ordering = ('start_datetime',)

    # ✅ Show Map Widget for activity_location & activity_meeting_location
    gis_widget_kwargs = {
        "attrs": {
            "default_lon": 0,  # Default longitude (adjust as needed)
            "default_lat": 0,  # Default latitude (adjust as needed)
            "default_zoom": 12  # Default zoom level
        }
    }

    formfield_overrides = {
        'activity_location': {'widget': OSMGeoAdmin.gis_widget_class},
        'activity_meeting_location': {'widget': OSMGeoAdmin.gis_widget_class},
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
