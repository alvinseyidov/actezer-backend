from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework import permissions, serializers, status, viewsets, generics
from .serializers import *
from account.models import *
from random import randrange
import requests

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_serializer = UserDetailSerializer(user)

        if user:
            return Response({
                "status": 200,
                "message": "user signed in",
                "success": True,
                "data": user_serializer.data
            })
        else:
            return Response({
                "status": 401,
                "message": "user didn't sign in",
                "success": False,
                "data": None
            }, status=401)



class RegisterView(APIView):
    def post(self, request):
        URL = "https://www.poctgoyercini.com/api_http/sendsms.asp"
        temp_pass = randrange(1000, 9999)

        # Create a mutable copy of request.data
        data = request.data.copy()
        data['password'] = temp_pass

        username = data.get('username')
        user = CustomUser.objects.filter(username=username).first()

        if username == '994552466822':
            if user is None:
                temp_passadmin = 1234
                serializer = UserCreateSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                u = serializer.save()
                uv = CustomUser.objects.get(username=username)
                uv.set_password(str(temp_passadmin))
                uv.save()
                return Response({
                    'id': u.id,
                    'message': 'User created and OTP sent',
                    'password': temp_passadmin
                })
            else:
                temp_pass2 = randrange(1000, 9999)
                temp_passadmin = 1234
                u = CustomUser.objects.get(username=username)
                u.set_password(str(temp_passadmin))
                u.save()
                return Response({
                    'id': u.id,
                    'message': 'User exists and OTP sent',
                    'password': temp_passadmin
                })
        else:
            if user is None:
                PARAMS = {
                    'user': 'vvebrain_smpp',
                    'password': 'vvebrain456',
                    'gsm': username,
                    'text': temp_pass,
                }
                serializer = UserCreateSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                u = serializer.save()
                r = requests.get(url=URL, params=PARAMS)
                return Response({
                    'id': u.id,
                    'message': 'User created and OTP sent',
                    'password': temp_pass
                })

            else:
                temp_pass2 = randrange(1000, 9999)
                PARAMS = {
                    'user': 'vvebrain_smpp',
                    'password': 'vvebrain456',
                    'gsm': username,
                    'text': temp_pass2,
                }

                u = CustomUser.objects.get(username=username)
                u.set_password(str(temp_pass2))
                u.save()
                r = requests.get(url=URL, params=PARAMS)
                return Response({
                    'id': u.id,
                    'message': 'User exists and OTP sent',
                    'password': temp_pass2
                })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)



class UserAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()




class UserListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserListSerializer
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return CustomUser.objects.filter(profile_image__isnull=False)

class UserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer
    authentication_classes = [TokenAuthentication]
    lookup_field = 'pk'

class UserUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    authentication_classes = [TokenAuthentication]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response({"message": "failed", "details": serializer.errors})




class InterestListView(ListAPIView):
    serializer_class = InterestListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search_query = self.request.query_params.get('search', None)
        if search_query and len(search_query) >= 1:
            return Interest.objects.filter(name__icontains=search_query).order_by('name')[:5]
        return Interest.objects.none()







class UserImageCreateView(generics.CreateAPIView):
    """
    API to add a new image for the authenticated user.
    """
    queryset = UserImage.objects.all()
    serializer_class = UserImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserImageDeleteView(APIView):
    """
    API to delete a user's image.
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        try:
            user_image = UserImage.objects.get(pk=pk, user=request.user)
            user_image.delete()
            return Response({"message": "Image deleted successfully."}, status=200)
        except UserImage.DoesNotExist:
            return Response({"error": "Image not found or does not belong to you."}, status=404)



class UserRatingCreateView(generics.CreateAPIView):
    """
    API to create a user rating.
    """
    queryset = UserRating.objects.all()
    serializer_class = UserRatingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserRatingDeleteView(APIView):
    """
    API to delete a user rating.
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        try:
            rating = UserRating.objects.get(pk=pk, rated_by=request.user)
            rating.delete()
            return Response({"message": "Rating deleted successfully."}, status=200)
        except UserRating.DoesNotExist:
            return Response({"error": "Rating not found or you are not authorized to delete it."}, status=404)