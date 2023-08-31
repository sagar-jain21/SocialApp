from rest_framework import serializers

from authentication.serializers import UserDataSerializer
from core.models import Comment, Follow, Like, Post


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    user = UserDataSerializer()

    class Meta:
        model = Post
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"


class FollowersSerializer(serializers.ModelSerializer):
    user = UserDataSerializer()

    class Meta:
        model = Follow
        fields = ["uuid", "user"]


class FollowingsSerializer(serializers.ModelSerializer):
    user_following = UserDataSerializer()

    class Meta:
        model = Follow
        fields = ["uuid", "user_following"]
