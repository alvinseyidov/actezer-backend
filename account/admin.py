from django.contrib import admin
from .models import CustomUser, UserImage, Interest, UserRating


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'country', 'city', 'birthday', 'activity_radius')
    search_fields = ('username', 'email', 'country__name', 'city__name')
    list_filter = ('country', 'city')
    ordering = ('username',)


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