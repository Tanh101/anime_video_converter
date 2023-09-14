from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadForm
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
import boto3

def upload(request):
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
            return redirect('details')
        else:
            for field, err in upload_form.errors.items():
                messages.error(request, err)

    else:
        upload_form = UploadForm()

    return render(request, 'home/upload.html', {'upload_form': upload_form})

def details(request):
    return render(request, "home/details.html")
