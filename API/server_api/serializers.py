from rest_framework import serializers
from .models import Post, Calli
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'title',
            'subtitle',
            'content',
            'created_at',
        )
        read_only_fields = ('created_at',)

class CalliSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calli
        fields = (
            'id',
            'name',
            'param1',
            'param2',
            'param3',
            'created_at',
        )
        read_only_fields = ('created_at',)

