from django.conf.urls import include
from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'account-api'

urlpatterns = [
    path('login/', CustomAuthToken.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('interest/list/', InterestListView.as_view(), name="interest-list"),
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name="user-update"),
    path('user/<int:pk>/', UserDetailView.as_view(), name="user-detail"),
    path('user/list/', UserListView.as_view(), name="user-list"),

    path('ratings/create/', UserRatingCreateView.as_view(), name='user-rating-create'),
    path('ratings/delete/<int:pk>/', UserRatingDeleteView.as_view(), name='user-rating-delete'),
]