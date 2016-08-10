from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import BlogPost, Comment
from .forms import PostForm, CommentForm
from .admin import UserCreationForm
from customauth.models import MyUser


# Create your views here.
def index(request):
    return render(request, 'website/index.html', {'blogs': BlogPost.objects.all()})


def post_detail(request, post_id):
    post = BlogPost.objects.get(pk=post_id)
    return render(request, 'website/post_detail.html', {'post': post})


def create_post(request):
    if not request.user.is_authenticated():
        return redirect('website:login')
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
        user.activation_code = generate_activation_url()
        user.is_active = False
        user.save()

        # generate email
        msg_plain = 'hi'
        msg_html = render_to_string('website/activate.html', {'user': user, 'code': user.activation_code})
        send_mail('Activate Acount', msg_plain, 'chasevedder@gmail.com', ['chasevedder@gmail.com',], html_message=msg_html)

        password = request.POST['password2']
        username = user.email
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('website:index')

        return redirect('website:login')
    context = {
        "form": form,
    }
    return render(request, 'website/register.html', context)


def create_comment(request, post_id):
    if not request.user.is_authenticated():
        return redirect('website:login')
    else:
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = BlogPost.objects.get(pk=post_id)
            comment.author = request.user

            comment.save()
            return redirect('website:post-detail', post_id=post_id)
        context = {
            "form": form,
            "post": BlogPost.objects.get(pk=post_id)
        }
        return render(request, 'website/create_comment.html', context)


def reply_comment(request, post_id, comment_id):
    if not request.user.is_authenticated():
        return redirect('website:login')
    else:
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.parent = Comment.objects.get(pk=comment_id)
            comment.post = comment.parent.post
            comment.author = request.user

            comment.save()
            return redirect('website:post-detail', post_id=post_id)
        context = {
            "form": form,
            "post": BlogPost.objects.get(pk=post_id),
            "comment": Comment.objects.get(pk=comment_id)
        }
        return render(request, 'website/create_comment.html', context)


def generate_activation_url():
    code = get_random_string(32)
    try:
        user = MyUser.objects.get(activation_code=code)
    except MyUser.DoesNotExist:
        return code
    return generate_activation_url()


def activate_user(request, activation_code):
    try:
        user = MyUser.objects.get(activation_code=activation_code)
        user.is_active = True
        user.save()
        return redirect('website:login')
    except MyUser.DoesNotExist:
        return redirect('website:register')
