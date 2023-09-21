from django.shortcuts import get_object_or_404, redirect, render

def landing_page(request):
    return render(request, 'landing_page/landing_page.html')