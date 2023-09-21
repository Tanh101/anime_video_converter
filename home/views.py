from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import UploadForm
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
import boto3
from boto3.s3.transfer import S3Transfer
from .models import Video
from django.core.paginator import Paginator
import threading
from django.core.cache import cache
import uuid
from tempfile import NamedTemporaryFile
import shutil

# Upload progress tracking
def progress_callback(bytes_transferred, cache_key):
    current_progress = cache.get(cache_key, 0)
    new_progress = current_progress + bytes_transferred
    cache.set(cache_key, new_progress)

# Separate thread for uploading
def threaded_upload(s3_client, temp_file_path, s3_video_key, cache_key):
    transfer = S3Transfer(s3_client)
    transfer.upload_file(temp_file_path, settings.AWS_STORAGE_BUCKET_NAME, s3_video_key, 
                        callback=lambda x: progress_callback(x, cache_key))

def upload(request):
    user_email = request.session.get('user_email').split('@')[0]
    if request.method == 'POST':
        upload_form = UploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            # ...
            video_file = request.FILES['file']
            s3_video_key = f"videos/{video_file.name}"
            cache_key = str(uuid.uuid4())
            
            # Initialize progress in cache
            cache.set(cache_key, 0)
            cache.set(f"{cache_key}_total", video_file.size)

            # Save cache_key to session for tracking upload progress
            request.session['upload_cache_key'] = cache_key
            
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

            t = threading.Thread(target=threaded_upload, args=(s3_client, temp_file.name, s3_video_key, cache_key))
            t.start()
            # ...
            return redirect('details', page_num=1, video_name=video_file.name.split('.')[0])
    else:
        upload_form = UploadForm()

    return render(request, 'home/upload.html', {'upload_form': upload_form, 'user_email' : user_email})

# Add a Django view to return the upload progress
def upload_progress_view(request):
    cache_key = request.session.get('upload_cache_key', '')
    progress = cache.get(cache_key, 0)
    total_size = cache.get(f"{cache_key}_total", 1)  # Use 1 to avoid division by zero
    percentage = (progress / total_size) * 100
    return JsonResponse({"progress": percentage})

def details(request, page_num, video_name=''):
    user_id = request.session.get('user_id')
    user_email = request.session.get('user_email').split('@')[0]

    if(not user_id):
        return redirect("/login")
    
    items_per_page = 5

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
    

    return render(request, 'home/details.html', {'page_num' : page_num, 'page': page, 'total_count': total_count, 'total_page': total_page, 'page_array': page_array, 'user_email' : user_email, 'video_name': video_name})
