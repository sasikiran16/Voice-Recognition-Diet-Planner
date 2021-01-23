from django.shortcuts import render
from .models import Post


def home(request):
   
    return render(request, 'blog/home.html')


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def services(request):
    return render(request, 'blog/services.html', {'title': 'About'})

def test(request):
    return render(request, 'blog/test.html', {'title': 'About'})

def blog(request):
    return render(request, 'blog/blog.html', {'title': 'About'})


