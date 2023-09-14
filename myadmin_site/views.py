from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from rest_framework import permissions, status
from .serializers import VideoSerializer, UserSerializer
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
    return JsonResponse({'message': 'User was deleted successfully!'}, safe=False, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def ban_user(request, id):
    user = get_object_or_404(MyUser, id=id)
    if user.status == 'Banned':
        user.status = 'Active'
        user.save()
        return JsonResponse({'message': 'User has been unbanned successfully'}, safe=False, status=status.HTTP_200_OK)
    else:
        user.status = 'Banned'
        user.save()
        return JsonResponse({'message': 'User has been banned successfully'}, safe=False, status=status.HTTP_200_OK)

# Create your views here.
def dashboard(request):
    return render(request, "myadmin_site/index.html")
