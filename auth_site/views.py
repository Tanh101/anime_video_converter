from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import User
def login(request): 
    return render(request, "auth_site/login.html")
from django.contrib.auth.hashers import make_password

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Sử dụng make_password để mã hóa mật khẩu
            hashed_password = make_password(password)

            # Tạo người dùng mới và lưu vào cơ sở dữ liệu với mật khẩu đã mã hóa
            user = User(Email=email, Password=hashed_password)
            user.save()

            # Chuyển hướng sau khi đăng ký thành công
            return redirect('login')  # Điều hướng đến trang đăng nhập (cần thiết phải có URL 'login')
        else:
            print(form.errors)

    else:
        form = RegistrationForm()

    return render(request, "auth_site/register.html", {'form': form})
