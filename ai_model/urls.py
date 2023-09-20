from django.urls import path
from ai_model import views

urlpatterns = [
    path("process", views.process, name="process"),
]
