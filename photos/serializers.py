from rest_framework import serializers
from .models import Photo, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

from django.contrib.auth import get_user_model
User = get_user_model()

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]

class PhotoSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    users_tagged = SimpleUserSerializer(many=True, read_only=True)
    is_favorite=serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = "__all__"
        read_only_fields = ["photo_id", "uploaded_by"]

    def get_is_favorite(self,obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False

        return obj.favorited_by.filter(id=request.user.id).exists()
    
class PhotoListSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Photo
        fields = [
            "photo_id",
            "thumbnail_img",
            "original_img",
            "is_processed",
            "download_count",
        ]
    