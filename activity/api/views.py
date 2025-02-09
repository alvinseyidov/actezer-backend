from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from activity.models import Activity, ActivityParticipant, ActivityComment, ActivityChatMessage
from .serializers import (
    ActivitySerializer, ActivityParticipantSerializer,
    ActivityParticipantStatusSerializer, ActivityCommentSerializer,
    ActivityChatMessageSerializer
)
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from activity.models import Activity, ActivityParticipant
from rest_framework import status

# Activity Views




class ActivityListCreateView(generics.ListCreateAPIView):
    """
    API to list and create activities, filtered within user radius.
    """
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user

        if user.map_location_point:
            try:
                # 🔥 Ensure activity_radius is an integer
                user_radius = int(user.activity_radius) if user.activity_radius else 10  # Default 10km if empty
            except ValueError:
                user_radius = 10  # Default radius in case of a conversion error

            # ✅ Use the existing PointField directly
            user_location = user.map_location_point  # No need to manually create a Point

            # Filter activities within radius
            return (
                Activity.objects.annotate(
                    distance=Distance('location', user_location)  # Ensure `location` is a PointField
                )
                .filter(distance__lte=user_radius * 1000)  # ✅ Converts km to meters
                .exclude(created_by=user)  # ✅ Excludes user's own activities
                .order_by('distance')  # ✅ Orders by nearest
            )

        # If user has no location set, return all activities except their own
        return Activity.objects.exclude(created_by=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        

class ActivityParticipantDeleteView(DestroyAPIView):
    """
    API for a user to cancel their join request.
    """
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return ActivityParticipant.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        activity_id = request.query_params.get('activity')
        if not activity_id:
            return Response({"error": "Activity ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        participant = self.get_queryset().filter(activity_id=activity_id).first()
        if not participant:
            return Response({"error": "Join request not found"}, status=status.HTTP_404_NOT_FOUND)

        participant.delete()
        return Response({"message": "Join request canceled"}, status=status.HTTP_204_NO_CONTENT)

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
