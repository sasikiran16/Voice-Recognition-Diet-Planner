"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', include('blog.urls')),
    
    # path('userdetail/',user_views.indext, name='userdetail'), 
    path('demo/', user_views.demo, name='demo'),  
    path('goals/',user_views.goals, name='goals'),
    path('food_items/',user_views.food_items, name='food_items'),
    path('intermediate/',user_views.intermediate, name='intermediate'), 
    path('demographics/',user_views.demographics, name='demographics'),  
    path('tdee/', user_views.tdee, name='tdee'),  
    path('preference/', user_views.preference, name='preference'),
    path('record/',user_views.record, name='record'),
    path('voicereg/',user_views.voicereg, name='voicereg'),
    path('measurements/',user_views.measurements, name='measurements'),
    path('Breakfast/',user_views.breakfast, name='breakfast'),
    path('Lunch/',user_views.lunch, name='lunch'),
    path('Snacks/',user_views.snacks, name='snacks'),
    path('Dinner/',user_views.dinner, name='dinner'),
    path('total/',user_views.total, name='total'),
    path('update_userdets/',user_views.update_userdets, name='update_userdets'),
    path('update_fitness/',user_views.update_fitness, name='update_fitness'),
    path('food_info/',user_views.food_info, name='food_info'),
    path('graph/',user_views.graph, name='graph'),
    path('water/',user_views.water, name='water')

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
