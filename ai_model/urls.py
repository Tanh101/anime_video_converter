from django.urls import path
from ai_model import views
from auth_site import views as auth_views

urlpatterns = [
    path("process", views.process, name="process"),
]
