from django.contrib import admin
from .models import Activity, ActivityParticipant, ActivityComment, ActivityChatMessage


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'city', 'start_datetime', 'end_datetime', 'status', 'created_by')
    search_fields = ('name', 'category__name', 'city__name', 'created_by__username')
    list_filter = ('status', 'is_public', 'city', 'category')
    ordering = ('-start_datetime',)


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
