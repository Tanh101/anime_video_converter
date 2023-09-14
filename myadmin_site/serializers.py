from rest_framework.serializers import ModelSerializer
from home.models import Video
from auth_site.models import User

class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = ['Id', 'User_Id', 'Original_video_path', 'Converted_video_path', 'Status', 'Created_at', 'Update_at']
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['Id', 'Email', 'Password', 'Role', 'Status', 'Created_at', 'Update_at']
