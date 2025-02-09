from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models

class CustomUser(AbstractUser):
    GENDER = (
        ('M','Male'),
        ('F','Female'),
    )
    email = models.EmailField(unique=True, blank=True, null=True)
    gender = models.CharField(max_length=2, choices=GENDER, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    country = models.ForeignKey('core.Country', on_delete=models.SET_NULL, null=True, blank=True,)
    city = models.ForeignKey('core.City', on_delete=models.SET_NULL, null=True, blank=True,)
    birthday = models.DateField(blank=True, null=True)

    map_location_point = models.PointField(geography=True, blank=True, null=True)
    map_location_address = models.CharField(max_length=256,blank=True, null=True)  # Store latitude and longitude as JSON
    activity_radius = models.PositiveIntegerField(default=10)  # Radius in kilometers
    interests = models.ManyToManyField('Interest', blank=True)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class UserImage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='user_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"


class Interest(models.Model):
    name = models.CharField(max_length=100)
    icon = models.FileField()

    def __str__(self):
        return self.name


class UserRating(models.Model):
    rated_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_ratings')
    rated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_ratings')
    rating = models.PositiveIntegerField(default=0, choices=[(i, f'{i} Star') for i in range(1, 6)])  # 1 to 5 stars
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rated_user', 'rated_by')  # Ensure one user can't rate another multiple times
        verbose_name = "User Rating"
        verbose_name_plural = "User Ratings"

    def __str__(self):
        return f"{self.rated_by.username} rated {self.rated_user.username} ({self.rating} stars)"
