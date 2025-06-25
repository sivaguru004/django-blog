from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from blogApp.models import Catagory, Post

class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100, required=True)
    email = forms.EmailField(label = 'Email', required=True)
    message = forms.CharField(label='Message', required=True)

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=100, required=True)
    email = forms.EmailField(label='Email', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)
    password_confirm = forms.CharField(label='Confirm Password', max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cData = super().clean()
        pwd = cData.get('password')
        cPwd = cData.get('password_confirm')

        if pwd:
            if len(pwd)<6:
                raise forms.ValidationError('Minimum Length of Password must be 6')
            if not any(i in '!@#$%^&*()_+-' for i in pwd):
                raise forms.ValidationError('Password must Contain at leat one Special Character')
            if not any(i.isupper()  for i in pwd):
                raise forms.ValidationError('Password must Contain at leat one UpperCase')
            if not any(i.islower()  for i in pwd):
                raise forms.ValidationError('Password must Contain at leat one UpperCase')
            if pwd != cPwd:
                raise forms.ValidationError('Confirm Password do not Match')
        
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, required=True)

    def clean(self):
        cData = super().clean()
        username = cData.get('username')
        pwd = cData.get('password')
        if username and pwd:
            user = authenticate(username=username, password=pwd)
            if user is None:
                raise forms.ValidationError('Username or Password is Wrong')

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=250, required=True)

    def clean(self):
        cData = super().clean()
        email = cData.get('email')

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('No user register with this Email.')

class ResetPasswordForm(forms.Form):
    npwd = forms.CharField(label='New Password', min_length=6, required=True)
    cpwd = forms.CharField(label='Confirm Password', min_length=6, required=True)

    def clean(self):
        cData = super().clean()
        new_password = cData.get('npwd')
        confirm_password = cData.get('cpwd')

        if new_password:
            if len(new_password) < 6:
                raise forms.ValidationError('Minimum Length of Password must be 6')
            if not any(i in '!@#$%^&*()_+-' for i in new_password):
                raise forms.ValidationError('Password must contain at least one special character')
            if not any(i.isupper() for i in new_password):
                raise forms.ValidationError('Password must contain at least one uppercase letter')
            if not any(i.islower() for i in new_password):
                raise forms.ValidationError('Password must contain at least one lowercase letter')
            if new_password != confirm_password:
                raise forms.ValidationError('Confirm Password does not match')
            
# class PostForm(forms.ModelForm):
#     title = forms.CharField(label='Title', max_length=200, required=True)
#     Content = forms.CharField(label='Content')
#     catagory = forms.ModelChoiceField(label='Catagory', required=True, queryset=Catagory.objects.all())

#     class Meta:
#         model = Post
#         fields = ['title', 'content', 'catagory', 'img_url']

#     def clean(self):
#         cData = super().clean()
#         title = cData.get('title')
#         con

#         if title and len(title)<5:
#             raise forms.ValidationError('The length of Title must be 5 Character.')
        
#         if content and len(content)<10:
#             raise forms.ValidationError('The length of Content must be 10 Character.')