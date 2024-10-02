from django.shortcuts import render
from .services import get_embed_map_url
from django.conf import settings
from django.contrib.auth.views import PasswordResetView

# views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

def home(request):
    return render(request, 'ATLFoodFinder/home.html')
def map(request):
    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    print(context)
    return render(request, 'ATLFoodFinder/map.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Specify the backend explicitly
            backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user, backend=backend)

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
    if request.method == 'POST':
        user = request.user
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Update the user's email (username)
        if email and email != user.email:
            user.email = email
            user.username = email  # Also update the username
            user.save()

        # Update the user's password (if provided)
        if password:
            user.set_password(password)
            user.save()
            # Required to keep the user logged in after password change
            update_session_auth_hash(request, user)

        return redirect('profile')

    return render(request, 'ATLFoodFinder/profile.html')
