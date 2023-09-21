from django.urls import path
from landing_page import views as landing_page

urlpatterns = [
    path("", landing_page.landing_page, name="landing_page"),
]
