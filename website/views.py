from django.shortcuts import render, redirect
from django.contrib.auth import logout

from .models import BlogPost
from .forms import PostForm


# Create your views here.
def index(request):
    return render(request, 'website/index.html', {'blogs': BlogPost.objects.all()})


def post_detail(request, post_id):
    post = BlogPost.objects.get(pk=post_id)
    return render(request, 'website/post_detail.html', {'post': post})


def create_post(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
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
