from rest_framework.serializers import ModelSerializer
from home.models import Video
from auth_site.models import MyUser

class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = ['Id', 'User_Id', 'Original_video_path', 'Converted_video_path', 'Status', 'Created_at', 'Update_at']
        
class UserSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['Id', 'Email', 'Password', 'Role', 'Status', 'Created_at', 'Update_at']
