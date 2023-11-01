from django.shortcuts import get_object_or_404, redirect, render

def landing_page(request):
    user_id = request.session.get('user_id')
    if(not user_id):
        return render(request, 'landing_page/landing_page.html')
    return redirect('upload')