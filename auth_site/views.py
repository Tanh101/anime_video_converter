from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import MyUser
def login(request): 
    return render(request, "auth_site/login.html")
from django.contrib.auth.hashers import make_password
from myadmin_site.views import dashboard
# def login(request): 
#     return render(request, "auth_site/login.html")
# @login_required
# def login(request):
#     user_role = request.MyUser.Role
#     if user_role == 'user':
#         # Điều hướng sang trang dashboard cho tài khoản admin
#         return render(request, "auth_site/register.html")
#     else:
#         # Điều hướng mặc định hoặc thông báo lỗi cho các vai trò khác
#         return redirect('dashboard')
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from .models import MyUser

def login(request):
    if request.method == 'POST':
        # Nhận đầu vào từ người dùng
        email = request.POST['email']
        password = request.POST['password']

        try:
            # Tìm tài khoản dựa trên địa chỉ email
            user = MyUser.objects.get(Email=email)

            # Kiểm tra mật khẩu
            if check_password(password, user.Password):
                # Đăng nhập thành công, kiểm tra trường Role
                if user.Role == 'user':
                    # Điều hướng sang trang admin
                    return redirect('register')
                else:
                    # Điều hướng sang trang user
                    return redirect('dashboard')
            else:
                # Mật khẩu không đúng, thông báo lỗi
                return render(request, 'auth_site/login.html', {'error_message': 'Mật khẩu không đúng'})
        except MyUser.DoesNotExist:
            # Không tìm thấy tài khoản với địa chỉ email này, thông báo lỗi
            return render(request, 'auth_site/login.html', {'error_message': 'Tài khoản không tồn tại'})

    # Nếu là GET request hoặc không thành công, hiển thị trang đăng nhập
    return render(request, 'auth_site/login.html')

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
