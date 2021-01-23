from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('services/', views.services, name='blog-services'),
    path('test/', views.test, name='blog-test'),
    path('blog/', views.blog, name='blog-blog')
    
]
