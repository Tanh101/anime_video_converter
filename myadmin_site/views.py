from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import permissions, status
from serializers import VideoSerializer, UserSerializer
from rest_framework.decorators import api_view
from home.models import Video
from auth_site.models import MyUser
from django.core.paginator import Paginator

@api_view(['GET'])  
def video_list(request):
    page_number = request.GET.get('page', 1)
    videos = Video.objects.all()
    items_per_page = 10 
    paginator = Paginator(videos, items_per_page)
    page = paginator.get_page(page_number)
    serializer = VideoSerializer(page, many=True)
    response_data = {
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'results': serializer.data,
    }
    return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
def vide_detail(request, id):
    video = Video.objects.get(Id=id)
    serializer = VideoSerializer(video)
    return JsonResponse({'result': serializer.data}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_list(request):
    page_number = request.GET.get('page', 1)
    users = MyUser.objects.all()
    items_per_page = 10  
    paginator = Paginator(users, items_per_page)
    page = paginator.get_page(page_number)
    serializer = UserSerializer(page, many=True)
    response_data = {
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'results': serializer.data,
    }
    return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_user(request, id):
    user = MyUser.objects.get(Id=id)
    user.delete()
    return JsonResponse({'message': 'User was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

# Create your views here.
def dashboard(request):
    return render(request, "myadmin_site/index.html")
