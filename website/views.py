from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
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
            if user.is_activated:
                login(request, user)
                return redirect('website:index')
            else:
                return render(request, 'website/login.html', {'error_message': 'You must activate your account before logging in'})
        else:
            return render(request, 'website/login.html', {'error_message': 'Invalid login'})
    return render(request, 'website/login.html')


def register_user(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.activation_code = generate_activation_url()
        user.save()

        # generate email
        msg_plain = 'hi'
        msg_html = render_to_string('website/activate.html', {'user': user, 'code': user.activation_code})
        send_mail('Activate Acount', msg_plain, 'chasevedder@gmail.com', [user.email,], html_message=msg_html)

        password = request.POST['password2']
        username = user.email
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('website:index')

        return redirect('website:register-success')
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
        user.is_activated = True
        user.save()
        return render(request, 'website/user_activated.html')
    except MyUser.DoesNotExist:
        return redirect('website:register')


def register_success(request):
    return render(request, 'website/account_creation_success.html', {})


def upvote(request):
    post_id = request.POST.get('post_id')
    vote_type = request.POST.get('type')
    action = request.POST.get('action')

    post = get_object_or_404(BlogPost, pk=post_id)

    upvotes = post.upvotes.filter(id=request.user.id).count()
    downvotes = post.downvotes.filter(id=request.user.id).count()

    if action == 'vote':
            if vote_type == 'up':
                post.upvotes.add(request.user)
                post.downvotes.remove(request.user)
            elif vote_type == 'down':
                post.upvotes.remove(request.user)
                post.downvotes.add(request.user)
            else:
                return HttpResponse('500 - unknown vote type' + vote_type)
    elif action == 'recall-vote':
        if vote_type == 'up':
            post.upvotes.remove(request.user)
        elif vote_type == 'down':
            post.downvotes.remove(request.user)
        else:
            return HttpResponse('500 - unknown vote type or no vote to recall' + vote_type)
    else:
        return HttpResponse('500 - bad action')
    post.score = post.upvotes.count() - post.downvotes.count()
    post.save()
    return HttpResponse(post.score)
