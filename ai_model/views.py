from django.shortcuts import render

# Create your views here.
def process(request):
    if request == "POST":
        email = request.GET['email']
        
    return render(request, 'ai_model/demo.html' )