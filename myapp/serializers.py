from rest_framework import serializers
from .models import CustomUser, Talk

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'account_image')

class TalkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talk
        fields = ('content', 'pub_date')