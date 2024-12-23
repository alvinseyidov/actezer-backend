from django.conf.urls import include
from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'activity-api'

urlpatterns = [
    # Activity endpoints
    path('activities/', ActivityListCreateView.as_view(), name='activity-list-create'),
    path('activities/<int:pk>/', ActivityDetailView.as_view(), name='activity-detail'),

    # Participant endpoints
    path('participants/request/', ActivityParticipantRequestView.as_view(), name='participant-request'),
    path('participants/update/<int:pk>/', ActivityParticipantUpdateStatusView.as_view(), name='participant-update-status'),

    # Comment endpoints
    path('comments/', ActivityCommentListCreateView.as_view(), name='comment-list-create'),

    # Chat message endpoints
    path('chat-messages/', ActivityChatMessageListCreateView.as_view(), name='chat-message-list-create'),
]