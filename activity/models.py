from django.contrib.gis.db import models
from account.models import CustomUser, Interest
from core.models import City  # Assuming City is in core app


class Activity(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=255)
    category = models.ForeignKey(Interest, on_delete=models.CASCADE, related_name='activities')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='activities')
    address = models.TextField()
    activity_location = models.PointField(geography=True, blank=True, null=True)  # Store latitude and longitude as JSON
    meeting_address = models.TextField()
    activity_meeting_location = models.PointField(geography=True, blank=True, null=True)  # Store latitude and longitude as JSON
    description = models.TextField(blank=True, null=True)
    people_limit = models.PositiveIntegerField()
    is_public = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_activities')

    def __str__(self):
        return self.name


class ActivityParticipant(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='joined_activities')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('activity', 'user')  # Prevent duplicate requests

    def __str__(self):
        return f"{self.user.username} - {self.activity.name} ({self.status})"



class ActivityComment(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activity_comments')
    content = models.TextField()
    rating = models.PositiveIntegerField(default=0, choices=[(i, f'{i} Star') for i in range(1, 6)])  # 1 to 5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.activity.name} (Rating: {self.rating})"



class ActivityChatMessage(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='chat_messages')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chat_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.user.username} in {self.activity.name}"
