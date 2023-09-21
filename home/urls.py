from django.urls import path
from home import views

urlpatterns = [
    path("upload", views.upload, name="upload"),
    path('details/<int:page_num>/<str:video_name>', views.details, name='details'),
    path('upload_progress', views.upload_progress_view, name='upload_progress'),
]
