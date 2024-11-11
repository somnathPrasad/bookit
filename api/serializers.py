from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("User with this email does not exist.")

            user = authenticate(username=user.username, password=password)

            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError("Incorrect password.")
        else:
            raise serializers.ValidationError("Must include both email and password.")

        return data
