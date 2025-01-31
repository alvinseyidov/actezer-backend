from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from account.models import *

User = get_user_model()



class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ['id', 'user', 'image', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']

    def validate_user(self, value):
        if self.context['request'].user != value:
            raise serializers.ValidationError("You can only manage your own images.")
        return value

class UserDetailSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'token',
            'first_name',
            'last_name',
            'country',
            'city',
            'map_location',
            'map_location_address',
            'profile_image',
            'age'
        )
    def get_age(self, obj):
        if obj.birthday:
            return (now().date() - obj.birthday).days // 365
        return None
    def get_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return token.key


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password',]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"




class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"



class InterestListSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    class Meta:
        model = Interest
        fields = ['id', 'name', 'icon']

    def get_icon(self, obj):
        request = self.context.get('request')
        if obj.icon:
            return request.build_absolute_uri(obj.icon.url)
        return None


class UserRatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRating
        fields = ['id', 'rated_user', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at', 'rated_by']

    def validate(self, data):
        rated_by = self.context['request'].user
        rated_user = data.get('rated_user')

        if rated_by == rated_user:
            raise serializers.ValidationError("You cannot rate yourself.")

        # Check if the user has already rated this user
        if UserRating.objects.filter(rated_by=rated_by, rated_user=rated_user).exists():
            raise serializers.ValidationError("You have already rated this user.")

        return data

    def create(self, validated_data):
        validated_data['rated_by'] = self.context['request'].user
        return super().create(validated_data)




from django.utils.timezone import now
class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'full_name', 'age', 'profile_image', 'city_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def get_age(self, obj):
        if obj.birthday:
            return (now().date() - obj.birthday).days // 365
        return None

    def get_profile_image(self, obj):
        request = self.context.get('request')
        if obj.profile_image and request:
            return request.build_absolute_uri(obj.profile_image.url)
        return None

    def get_city_name(self, obj):
        return obj.city.name if obj.city else None
