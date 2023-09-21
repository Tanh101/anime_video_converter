from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import MyUser
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import make_password
from myadmin_site.views import dashboard
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, JsonResponse
from rest_framework import permissions, status

@api_view(['GET', 'POST'])
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
                    user_updated_at = user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
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
                        return redirect('upload', )
                    else:
                        # Điều hướng sang trang admin
                       return redirect('dashboard')
            else:
                # Mật khẩu không đúng, thông báo lỗi
                return render(request, 'auth_site/login.html', {'error_message': 'Mật khẩu không đúng'})
        except MyUser.DoesNotExist:
            # Không tìm thấy tài khoản với địa chỉ email này, thông báo lỗi
            return render(request, 'auth_site/login.html', {'error_message': 'Tài khoản không tồn tại'})

    # Nếu là GET request hoặc không thành công, hiển thị trang đăng nhập
    return render(request, 'auth_site/login.html')

@api_view(['GET', 'POST'])
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

@api_view(['GET'])
def session_info(request):
    # Kiểm tra xem người dùng đã đăng nhập và có phiên làm việc không
    if 'user_id' in request.session and 'user_role' in request.session and 'user_email' in request.session and 'user_status' in request.session and 'user_created_at' in request.session and 'user_updated_at' in request.session:
        # Hiển thị thông tin về phiên làm việc
        user_session_data = {
            'id': request.session['user_id'],
            'role': request.session['user_role'],
            'email': request.session['user_email'],
            'status': request.session['user_status'],
            'created_at': request.session['user_created_at'],
            'update_at': request.session['user_updated_at'],
        }
        return JsonResponse(user_session_data, safe=False, status=status.HTTP_200_OK)
    else:
        # Phiên làm việc không tồn tại, đưa người dùng đến trang đăng nhập
        return redirect('login')
def logout_view(request):
    if 'user_id' in request.session:
        # Xóa hết các thông tin trong session
        request.session.clear()
        # Điều hướng đến trang đăng nhập sau khi logout
        return redirect('login')
    else:
        # Người dùng chưa đăng nhập, điều hướng đến trang đăng nhập
        return redirect('login')
