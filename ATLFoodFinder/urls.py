"""
URL configuration for ATLFoodFinder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
# urls.py

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from ATLFoodFinder import views
from .forms import CustomLoginForm
from .views import CustomPasswordResetConfirmView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='ATLFoodFinder/login.html', redirect_authenticated_user=True), name='login'),
    path('map/', views.map, name='map'),
    path('favorites/', views.favorites, name='favorites'),
    path('save_favorite/', views.save_favorite, name='save_favorite'),
    path('delete_favorite/', views.delete_favorite, name='delete_favorite'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='ATLFoodFinder/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='ATLFoodFinder/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', 
         CustomPasswordResetConfirmView.as_view(template_name='ATLFoodFinder/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='ATLFoodFinder/password_reset_complete.html'), name='password_reset_complete'),
]
