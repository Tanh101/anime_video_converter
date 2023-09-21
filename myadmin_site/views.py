from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from rest_framework import permissions, status
from .serializers import VideoSerializer, UserSerializer
from rest_framework.decorators import api_view
from home.models import Video
from auth_site.models import MyUser
from django.core.paginator import Paginator
import requests
import json
from django.core.cache import cache

@api_view(['GET'])  
def video_list(request, pageNumber):
    videos = Video.objects.all().order_by('id')
    if videos.count() == 0:
        response_data = {
        'results': [],
        'message': 'No videos found.'
        }
        return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)
    else:
        items_per_page = 10 
        paginator = Paginator(videos, items_per_page)
        page = paginator.get_page(pageNumber)
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
def user_list(request,pageNumber):
    users = cache.get('user_list')
    if users is None:
        users = MyUser.objects.all().order_by('id')
        cache.set('user_list', users, 600)

    if users.count() == 0:
        response_data = {
        'results': [],
        'message': 'No users found.'
        }
        return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)
    else:
        items_per_page = 10  
        paginator = Paginator(users, items_per_page)
        page = paginator.get_page(pageNumber)
        serializer = UserSerializer(page, many=True)
        response_data = {
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'results': serializer.data,
        }
        return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_user(request, id):
    user = MyUser.objects.get(id=id)
    user.delete()
    return JsonResponse({'message': 'User was deleted successfully!'}, safe=False, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def ban_user(request, id):
    user = get_object_or_404(MyUser, id=id)
    if user.status == 'banned':
        user.status = 'active'
        user.save()
        return JsonResponse({'message': 'User has been unbanned successfully'}, safe=False, status=status.HTTP_200_OK)
    else:
        user.status = 'banned'
        user.save()
        return JsonResponse({'message': 'User has been banned successfully'}, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
def search_users(request, pageNumber):
    searchEmail = request.GET.get('email', '')
    items_per_page = 10  
    # Perform a case-insensitive search for users with matching email
    users = MyUser.objects.all().filter(email__icontains=searchEmail).order_by('id')
    if(users.count() == 0):
        response_data = {
        'results': [],
        'message': 'No videos found with the given query.'
        }
        return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)
    else:
        paginator = Paginator(users, items_per_page)
        page = paginator.get_page(pageNumber)
        serializer = UserSerializer(page, many=True)
        response_data = {
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'results': serializer.data,
        }
        return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
def search_videos(request, pageNumber):
    query = request.GET.get('query', '')
    items_per_page = 10 
    videos = Video.objects.all().filter(original_video_path__icontains=query).order_by('id')
    if(videos.count() == 0):
        response_data = {
        'results': [],
        'message': 'No videos found with the given query.'
        }
        return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)
    else:
        paginator = Paginator(videos, items_per_page)
        page = paginator.get_page(pageNumber)
        serializer = VideoSerializer(page, many=True)
        response_data = {
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'results': serializer.data,
        }
        return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_page_info(request):
    Total_users = MyUser.objects.all().count();
    Total_videos = Video.objects.all().count();
    resposne_data = {
        'Total_users': Total_users,
        'Total_videos': Total_videos,
    }
    return JsonResponse(resposne_data, safe=False, status=status.HTTP_200_OK)

# Create your views here.
def dashboard(request):
    if(request.session.get('user_role') == 'admin'):
        return render(request, "myadmin_site/index.html",{
        'user_id': request.session.get('user_id'),
        'user_role': request.session.get('user_role'),
        'user_email': request.session.get('user_email'),
        'user_status': request.session.get('user_status'),
        })
    else:
        return redirect('login');
