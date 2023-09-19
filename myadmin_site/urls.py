from django.urls import path
from myadmin_site import views as myadmin_site

urlpatterns = [
    path("", myadmin_site.dashboard, name="dashboard"),
    path("videos/page=<int:pageNumber>", myadmin_site.video_list, name="api_videos"),  # Endpoint for fetching video data
    path("users/page=<int:pageNumber>", myadmin_site.user_list, name="api_users"),    # Endpoint for fetching user data
    path("users/<int:id>/delete/", myadmin_site.delete_user, name="api_delete_user"),  # Endpoint for deleting a user by ID
    path("videos/<int:id>/detail/", myadmin_site.vide_detail, name="api_video_detail"),  # Endpoint for fetching video details by ID
    path('users/<int:id>/ban/', myadmin_site.ban_user, name='ban_user'),
    path('search_users/page=<int:pageNumber>', myadmin_site.search_users, name='search_users'),
    path('search_videos/page=<int:pageNumber>', myadmin_site.search_videos, name='search_videos'),
    path('page_info/', myadmin_site.get_page_info, name='page_info'),
]
