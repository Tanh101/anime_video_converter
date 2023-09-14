from django import forms
from .models import User



class RegistrationForm(forms.Form):
    print(forms)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    print(password)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="confirm_password")
    # print(confirm_password)
    def clean(self):
        cleaned_data = super().clean()
        email = self.cleaned_data.get('email')
        if User.objects.filter(Email=email).exists():
            raise forms.ValidationError("Email đã tồn tại.")
        password = cleaned_data.get("password")
        print(password)
        confirm_password = cleaned_data.get("confirm_password")
        print(confirm_password)
        if password != confirm_password:
            raise forms.ValidationError("Mật khẩu không khớp.")
