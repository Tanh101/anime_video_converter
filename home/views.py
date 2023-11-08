from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import UploadForm
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from auth_site.models import MyUser
import boto3
from boto3.s3.transfer import S3Transfer
from .models import Video
from django.core.paginator import Paginator
import threading
from django.core.cache import cache
import uuid
from tempfile import NamedTemporaryFile
import shutil
import queue
import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import websockets
import asyncio
import json

# The queue to hold upload tasks
upload_queue = queue.Queue()

# The worker function
def worker():
    while True:
        task = upload_queue.get()
        if task is None:
            # sentinel value to exit loop
            break
        video, s3_client, temp_file_path, s3_video_key, cache_key, video_file_size = task
        print(f"Uploading {temp_file_path} to {s3_video_key}")
        cache.set(f"{cache_key}_status", "uploading")
        threaded_upload(video, s3_client, temp_file_path, s3_video_key, cache_key, video_file_size)
        while True:
            download_url = cache.get(f"{cache_key}_download_url")
            if download_url:
                upload_queue.task_done()
                break
            time.sleep(1)
        time.sleep(1)

# Number of worker threads
NUM_WORKERS = 1

# Start the worker threads
for i in range(NUM_WORKERS):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()
    print(f"Started worker thread {t.name}")

# Upload progress tracking
def progress_callback(bytes_transferred, cache_key):
    current_progress = cache.get(cache_key, 0)
    new_progress = current_progress + bytes_transferred
    # print(f"Progress: {new_progress}")
    cache.set(cache_key, new_progress)

# Separate thread for uploading
def threaded_upload(video, s3_client, temp_file_path, s3_video_key, cache_key, video_file_size):
    transfer = S3Transfer(s3_client)
    transfer.upload_file(temp_file_path, settings.AWS_STORAGE_BUCKET_NAME, s3_video_key, 
                        callback=lambda x: progress_callback(x, cache_key))
    # Explicitly set to 100% on completion
    cache.set(cache_key, video_file_size)

    download_url = "https://" + settings.CLOUDFRONT_DOMAIN + "/" + s3_video_key
    video.original_video_path = download_url
    video.status = "processing"
    video.save()
    # Send a message to the websocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'flask_group', 
        {
            'type': 'send_data_to_client',
            'message': {
                'video_url': download_url,
                'video_id': cache_key,
                'video_name': s3_video_key.split('/')[-1],
            }
        }
    )

    cache.set(f"{cache_key}_original_path", s3_video_key)

def upload(request):
    # user_email = request.session.get('user_email').split('@')[0]
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        upload_form = UploadForm(request.POST, request.FILES)
        if upload_form.is_valid():

            video_file = request.FILES['file']
            video_name = video_file.name
            video_extension = video_name.split('.')[-1]
            uuid_key = uuid.uuid4().hex
            s3_video_key = f"videos/{uuid_key}.{video_extension}"
        
            cache_keys = request.session.get('upload_cache_keys', [])

            user_instance = MyUser.objects.get(pk=user_id)
            
            video = Video(
                user=user_instance,
                name=video_file.name,
                status="uploading"
            )
            video.save()
            
            cache_key = str(video.id)  # Using the video's id as the cache key
            cache_keys.append(cache_key)

            # Initialize progress in cache
            cache.set(cache_key, 0)
            cache.set(f"{cache_key}_total", video_file.size)
            cache.set(f"{cache_key}_name", video_file.name)  # Storing video name in cache
            cache.set(f"{cache_key}_status", "queueing")

            # Save cache keys to session for tracking upload progress
            request.session['upload_cache_keys'] = cache_keys

            # Create a temporary file to save the uploaded file
            temp_file = NamedTemporaryFile(delete=False)
            for chunk in video_file.chunks():
                temp_file.write(chunk)
            temp_file.close()

            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            )

            # Add to queue instead of direct threading
            upload_queue.put((video, s3_client, temp_file.name, s3_video_key, cache_key, video_file.size))
            
            return redirect('details', page_num=1)
        else:
            for field, err in upload_form.errors.items():
                messages.error(request, err)
    else:
        upload_form = UploadForm()

    return render(request, 'home/upload.html', {'upload_form': upload_form})

def upload_progress_view(request):
    cache_keys = request.session.get('upload_cache_keys', [])
    # print(f"Cache keys from view: {cache_keys}")

    progress_data = []
    for cache_key in cache_keys:
        progress = cache.get(cache_key)
        total_size = cache.get(f"{cache_key}_total")
        video_name = cache.get(f"{cache_key}_name")
        original_path = cache.get(f"{cache_key}_original_path")
        download_url = cache.get(f"{cache_key}_download_url")
        # print(f"progress: {progress}, total_size: {total_size}")
        # download_url = None
        # if (original_path is not None):
        #     download_url = settings.CLOUDFRONT_DOMAIN + "/" + original_path

        # If any cache data is missing, skip this cache_key
        if None in [progress, total_size, video_name]:
            continue

        status = cache.get(f"{cache_key}_status")
        percentage = (progress / total_size) * 100

        file_data = {
            "key": cache_key,
            "progress": percentage,
            "video_id": cache_key,
            "name": video_name,
            "status": status
        }

        if download_url:
            video = Video.objects.get(pk=cache_key)
            video.converted_video_path = download_url
            video.status = "converted"
            video.save()
            file_data["download_url"] = download_url

        progress_data.append(file_data)

    return JsonResponse({"files": progress_data})


def details(request, page_num):
    user_id = request.session.get('user_id')
    user_email = request.session.get('user_email').split('@')[0]

    if(not user_id):
        return redirect("/login")
    
    items_per_page = 2

    start_index = (page_num - 1) * items_per_page
    end_index = start_index + items_per_page

    videos = Video.objects.filter(user_id=user_id).order_by('-updated_at')[start_index:end_index]

    total_count = Video.objects.filter(user_id=user_id).count()
    total_page = (total_count / items_per_page)
    tmp = round(total_page)
    if total_page > tmp:
        tmp = tmp + 1
    page_array = range(1, tmp + 1, 1)
    
    paginator = Paginator(videos, items_per_page)
    page = paginator.get_page(page_num)
    

    return render(request, 'home/details.html', {'page_num' : page_num, 'page': page, 'total_count': total_count, 'total_page': total_page, 'page_array': page_array, 'user_email' : user_email})
