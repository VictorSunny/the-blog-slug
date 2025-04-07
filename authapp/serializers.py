from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length= 100)
    username = serializers.CharField(max_length= 20)
    first_name = serializers.CharField(max_length= 25)
    last_name = serializers.CharField(max_length= 25)
    password = serializers.CharField(min_length= 8, write_only= True)

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password']

    def validate(self, attrs):

        duplicate_email = User.objects.filter(email= attrs['email']).exists()
        if duplicate_email:
            raise serializers.ValidationError(detail= "Sorry. This email is already taken by another user.")
        duplicate_username = User.objects.filter(username= attrs['username']).exists()
        if duplicate_username:
            raise serializers.ValidationError(detail= "Sorry. This username is already taken by another user.")
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        user = User.objects.create(
            username= validated_data['username'],
            first_name= validated_data['first_name'],
            last_name = validated_data['last_name'],
            email= validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user