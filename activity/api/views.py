from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from activity.models import Activity, ActivityParticipant, ActivityComment, ActivityChatMessage
from .serializers import (
    ActivitySerializer, ActivityParticipantSerializer,
    ActivityParticipantStatusSerializer, ActivityCommentSerializer,
    ActivityChatMessageSerializer
)


# Activity Views
class ActivityListCreateView(generics.ListCreateAPIView):
    """
    API to list and create activities.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API to retrieve, update, or delete an activity.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]


# Participant Views
class ActivityParticipantRequestView(generics.CreateAPIView):
    """
    API for a user to request to join an activity.
    """
    queryset = ActivityParticipant.objects.all()
    serializer_class = ActivityParticipantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ActivityParticipantUpdateStatusView(generics.UpdateAPIView):
    """
    API for the activity creator to accept or reject join requests.
    """
    queryset = ActivityParticipant.objects.all()
    serializer_class = ActivityParticipantStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ActivityParticipant.objects.filter(activity__created_by=self.request.user)


# Comment Views
class ActivityCommentListCreateView(generics.ListCreateAPIView):
    """
    API to list and create comments for an activity.
    """
    queryset = ActivityComment.objects.all()
    serializer_class = ActivityCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Chat Message Views
class ActivityChatMessageListCreateView(generics.ListCreateAPIView):
    """
    API to list and create chat messages for an activity.
    """
    queryset = ActivityChatMessage.objects.all()
    serializer_class = ActivityChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
