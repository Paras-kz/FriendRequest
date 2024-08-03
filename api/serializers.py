from rest_framework import serializers
from .models import CustomUser, FriendRequest
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True} #not to be fetched and serialized while reading
        }
    
    def validate_email(self, value):
        if CustomUser.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("user already exists with this email.")
        return value

    def create(self, validated_data):#it is called when serializer.save() is called
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'].lower(),
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('id', 'from_user', 'to_user', 'status', 'timestamp')
        read_only_fields = ['from_user', 'status', 'timestamp']

    def validate(self, data):
        request = self.context.get('request', None)
        if request:
            from_user = request.user
            to_user = data.get('to_user')
            if from_user == to_user:
                raise serializers.ValidationError("You cannot send a friend request to yourself.")
        return data


   

 