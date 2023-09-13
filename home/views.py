from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def upload(request):
    return render(request, "home/upload.html")

def details(request):
    return render(request, "home/details.html")
