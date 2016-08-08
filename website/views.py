from django.shortcuts import render

from .models import BlogPost

# Create your views here.
def index(request):
    return render(request, 'website/index.html', {'blogs': BlogPost.objects.all()})

def post_detail(request, post_id):
    post = BlogPost.objects.get(pk=post_id)
    return render(request, 'website/post_detail.html', {'post': post})