from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login

from .models import BlogPost
from .forms import PostForm, UserForm
from .admin import UserCreationForm


# Create your views here.
def index(request):
    return render(request, 'website/index.html', {'blogs': BlogPost.objects.all()})


def post_detail(request, post_id):
    post = BlogPost.objects.get(pk=post_id)
    return render(request, 'website/post_detail.html', {'post': post})


def create_post(request):
    if not request.user.is_authenticated():
        return redirect('website:index')
    else:
        form = PostForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('website:post-detail', post_id=post.pk)
        context = {
            "form": form,
        }
        return render(request, 'website/create_post.html', context)


def user_logout(request):
    logout(request)
    return redirect('website:index')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('website:index')
            else:
                return render(request, 'website/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'website/login.html', {'error_message': 'Invalid login'})
    return render(request, 'website/login.html')


def register_user(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
        password = request.POST['password2']
        username = user.email
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('website:index')
    context = {
        "form": form,
    }
    return render(request, 'website/register.html', context)