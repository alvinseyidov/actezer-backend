from rest_framework import serializers
from activity.models import Activity, ActivityParticipant, ActivityComment, ActivityChatMessage


class ActivitySerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    is_joined = serializers.BooleanField(read_only=True)
    is_requested = serializers.BooleanField(read_only=True)

    class Meta:
        model = Activity
        fields = [
            'id', 'name', 'category', 'start_datetime', 'end_datetime', 'city',
            'address', 'activity_location', 'meeting_address', 'activity_meeting_location',
            'description', 'people_limit', 'is_public', 'status', 'created_by',
            'is_joined', 'is_requested'  # ✅ New Fields
        ]
        read_only_fields = ['id', 'status', 'created_by', 'is_joined', 'is_requested']


class ActivityParticipantSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = ActivityParticipant
        fields = ['id', 'activity', 'user', 'status', 'joined_at']
        read_only_fields = ['id', 'user', 'joined_at', 'status']


class ActivityParticipantStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityParticipant
        fields = ['id', 'status']

    def validate_status(self, value):
        if value not in ['accepted', 'rejected']:
            raise serializers.ValidationError("Status must be 'accepted' or 'rejected'.")
        return value


class ActivityCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = ActivityComment
        fields = ['id', 'activity', 'user', 'content', 'rating', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class ActivityChatMessageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = ActivityChatMessage
        fields = ['id', 'activity', 'user', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
