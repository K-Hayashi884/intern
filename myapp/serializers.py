from rest_framework import serializers
from .models import CustomUser, Talk

""" 検索文を作る過程で作成、
結局有効には使えていないがjsに渡す時有用だという勉強になった"""
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'account_image')

class TalkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talk
        fields = ('content', )