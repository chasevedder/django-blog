from django.shortcuts import render

from .models import BlogPost

# Create your views here.
def index(request):
    return render(request, 'website/index.html', {'blogs': BlogPost.objects.all()})