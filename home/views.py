from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadForm
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
import boto3
from .models import Video
from django.core.paginator import Paginator

def upload(request):
    user_email = request.session.get('user_email').split('@')[0]
    if request.method == 'POST':
        upload_form = UploadForm(request.POST, request.FILES)

        if upload_form.is_valid():
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            )

            # Get the uploaded file
            video_file = request.FILES['file']

            # Generate a key (filename) for the uploaded video in S3
            s3_video_key = f"videos/{video_file.name}"

            # Upload the file to S3
            s3_client.upload_fileobj(
                video_file,
                settings.AWS_STORAGE_BUCKET_NAME,
                s3_video_key,
                ExtraArgs={
                    'ContentType': video_file.content_type,
                    'ACL': 'public-read',
                }
            )

            # Generate the URL where the video can be accessed on S3
            s3_video_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{s3_video_key}"

            # TODO: Save `s3_video_url` to your database
            messages.success(request, "Video uploaded successfully")
            return redirect('details', page_num=1)
        else:
            for field, err in upload_form.errors.items():
                messages.error(request, err)

    else:
        upload_form = UploadForm()

    return render(request, 'home/upload.html', {'upload_form': upload_form, 'user_email' : user_email})

def details(request, page_num):
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
    

    return render(request, 'home/details.html', {'page_num' : page_num, 'page': page, 'total_count': total_count, 'total_page': total_page, 'page_array': page_array, 'user_email' : user_email})
