from rest_framework.serializers import ModelSerializer
from home.models import Video
from auth_site.models import MyUser

class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'user_id', 'original_video_path', 'converted_video_path', 'status', 'created_at', 'update_at']
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'email', 'password', 'role', 'status', 'created_at', 'update_at']
