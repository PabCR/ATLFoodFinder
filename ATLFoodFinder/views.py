from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView

# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy

def home(request):
    return render(request, 'ATLFoodFinder/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # Redirect to profile page after registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'ATLFoodFinder/register.html', {'form': form})

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def get_success_url(self):
        # Redirect to home after password is reset
        return reverse_lazy('home')

@login_required
def profile(request):
    return render(request, 'ATLFoodFinder/profile.html')
