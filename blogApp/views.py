from django.shortcuts import render, redirect
from django.http import HttpResponse
import logging
from .models import Catagory, Post, AboutUs
from django.core.paginator import Paginator
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    blog_title = 'Latest Posts'
    all_posts = Post.objects.all()

    # Paginate
    paginator = Paginator(all_posts, 5)
    page_no = request.GET.get('page')
    page_object = paginator.get_page(page_no)

    return render(request, 'index.html', {'blog_title':blog_title, 'page_obj':page_object})

def detail(request, slug):
    post = Post.objects.get(slug = slug)
    related_posts = Post.objects.filter(catagory = post.catagory).exclude(pk=post.pk)
    # logger = logging.getLogger('TESTING')
    # logger.debug(f'post variable is {post}')
    return render(request, 'detail.html', {'post':post, 'related_posts':related_posts})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if form.is_valid():
            success_message = 'Your Email has been Send!'

            #Write Code For database
            #

            return render(request, 'contact.html', {'form':form, 'success_message':success_message})
        return render(request, 'contact.html', {'form':form, 'name':name, 'email':email, 'message':message})
    return render(request, 'contact.html')


def About(request):
    about = AboutUs.objects.first()
    if about is None or not about.content:
        about = 'There is no Content About Us'
    else:
        about = about.content
    return render(request, 'about.html', {'about_content':about})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration Successfull, You can Login Now!')
            return redirect('blog:login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form':form})

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('blog:dashboard')
    return render(request, 'login.html', {'form':form})

def dashboard(request):
    blogTitle = 'My Posts'
    # getting User Post
    all_posts = Post.objects.filter(user=request.user)

    # Paginate
    paginator = Paginator(all_posts, 5)
    page_no = request.GET.get('page')
    page_object = paginator.get_page(page_no)

    return render(request, 'dashboard.html', {'blogTitle':blogTitle, 'page_obj':page_object})

def logout(request):
    auth_logout(request)
    return redirect('blog:index')

# def forgotpwd(request):
#     form = ForgotPasswordForm() 
#     if request.method == 'POST':
#         form = ForgotPasswordForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             user = User.objects.filter(email=email)

#             #send email to reset email
#             token = default_token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             site = get_current_site(request)
#             domain = site.domain
#             subject = 'Reset Password Requested'
#             message = render_to_string('reset_password_email.html', {'domain':domain, 'uid':uid, 'token':token})
#             send_mail(subject, message, 'noreply@sivaguru.com', [email])
#             messages.success(request, 'Email has been sent successfully!')

#     return render(request, 'forgotpwd.html', {'form':form})
    
# def reset_password(request, uidb64, token):
#     form = ResetPasswordForm()
#     if request.method == 'POST':
#         form = ResetPasswordForm(request.POST)
#         if form.is_valid():
#             new_password = form.cleaned_data['new_password']
#             uid = urlsafe_base64_decode(uidb64)
#             try:
#                 user = User.objects.get(pk=uid)
#             except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#                 user = None

#             if user is not None and default_token_generator.check_token(user, token):
#                 user.set_password(new_password)
#                 user.save()
#                 messages.success(request, 'Your passwoard has been reset successfully!')
#                 return redirect('blog:login')
#             else:
#                 messages.error(request, 'The passward reset link is Invalid')

#     return render(request, 'reset_password.html', {'form':form})

# def newpost(request):
#     catagories = Catagory.objects.all()
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.user = request.user
#             post.save()
#             messages.success(request, "Post created successfully!")
#             return redirect('blog:dashboard')
#     else:
#         form = PostForm()
#     return render(request, 'newpost.html', {'catagories':catagories, 'form':form})

class newpost(LoginRequiredMixin, CreateView):
    model = Post
    fields = '__all__'
    success_url = reverse_lazy('blog:dashboard')
    template_name = 'newpost.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Post Created successfully! ✅')
        return super(newpost, self).form_valid(form)
    
class editpost(LoginRequiredMixin, UpdateView):
    model = Post
    fields = '__all__'
    template_name = 'editpost.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('blog:dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Post updated successfully! ✅')
        return super(editpost, self).form_valid(form)
    
@csrf_exempt
@login_required
def delete_post(request, slug):
    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            post = Post.objects.get(slug=slug, user=request.user)
            post.delete()
            return JsonResponse({'status': 'success'})
        except Post.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Post not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})