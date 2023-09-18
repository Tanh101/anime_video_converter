from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import MyUser
def login(request): 
    return render(request, "auth_site/login.html")
from django.contrib.auth.hashers import make_password
from myadmin_site.views import dashboard
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password

# def login(request):
#     if request.method == 'POST':
#         # Nhận đầu vào từ người dùng
#         email = request.POST['email']
#         password = request.POST['password']

#         try:
#             # Tìm tài khoản dựa trên địa chỉ email
#             user = MyUser.objects.get(email=email)

#             # Kiểm tra mật khẩu
#             if check_password(password, user.password):
#                 # Đăng nhập thành công, kiểm tra trường Role
#                 if user.role == 'user':
#                     # Điều hướng sang trang admin
#                     return redirect('upload')
#                 else:
#                     # Điều hướng sang trang user
#                     return redirect('dashboard')
#             else:
#                 # Mật khẩu không đúng, thông báo lỗi
#                 return render(request, 'auth_site/login.html', {'error_message': 'Mật khẩu không đúng'})
#         except MyUser.DoesNotExist:
#             # Không tìm thấy tài khoản với địa chỉ email này, thông báo lỗi
#             return render(request, 'auth_site/login.html', {'error_message': 'Tài khoản không tồn tại'})

#     # Nếu là GET request hoặc không thành công, hiển thị trang đăng nhập
#     return render(request, 'auth_site/login.html')

def login(request):
    if request.method == 'POST':
        # Nhận đầu vào từ người dùng
        email = request.POST['email']
        password = request.POST['password']


        try:
            # Tìm tài khoản dựa trên địa chỉ email
            user = MyUser.objects.get(email=email)

            # Kiểm tra mật khẩu
            if check_password(password, user.password):
                if user.status == 'active':
                    user_created_at = user.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    user_updated_at = user.update_at.strftime("%Y-%m-%d %H:%M:%S")
                    # Đăng nhập thành công, lưu thông tin người dùng vào phiên làm việc
                    request.session['user_id'] = user.id
                    request.session['user_role'] = user.role
                    request.session['user_email'] = user.email
                    request.session['user_status'] = user.status
                    request.session['user_created_at'] = user_created_at
                    request.session['user_updated_at'] = user_updated_at
                # Điều hướng tới trang tương ứng
                    if user.role == 'user':
                        # Điều hướng sang trang user
                        return redirect('dashboard')
                    else:
                        # Điều hướng sang trang admin
                        return redirect('upload')
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
            user = MyUser(email=email, password=hashed_password)
            user.save()

            # Chuyển hướng sau khi đăng ký thành công
            return redirect('login')  # Điều hướng đến trang đăng nhập (cần thiết phải có URL 'login')
        else:
            print(form.errors)

    else:
        form = RegistrationForm()

    return render(request, "auth_site/register.html", {'form': form})
def session_info(request):
    # Kiểm tra xem người dùng đã đăng nhập và có phiên làm việc không
    if 'user_id' in request.session and 'user_role' in request.session and 'user_email' in request.session and 'user_status' in request.session and 'user_created_at' in request.session and 'user_updated_at' in request.session:
        user_id = request.session['user_id']
        user_role = request.session['user_role']
        user_mail = request.session['user_email']
        user_status = request.session['user_status']
        user_created_at = request.session['user_created_at']
        user_updated_at = request.session['user_updated_at']
        # Hiển thị thông tin về phiên làm việc
        return render(request, 'auth_site/session_info.html', {'user_id': user_id, 'user_role': user_role, 'user_mail': user_mail, 'user_status': user_status, 'user_created_at': user_created_at, 'user_updated_at': user_updated_at})
    else:
        # Phiên làm việc không tồn tại, đưa người dùng đến trang đăng nhập
        return redirect('login')
