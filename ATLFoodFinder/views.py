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
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Restaurant, Favorite
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Restaurant, Favorite
import json


def home(request):
    return render(request, 'ATLFoodFinder/home.html')


@login_required
def favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('restaurant')
    context = {
        'favorites': favorites,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'ATLFoodFinder/favorites.html', context)



@csrf_exempt  # Allow CSRF exemption since we're handling it manually
def save_favorite(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'unauthenticated'})

    if request.method == 'POST':
        data = json.loads(request.body)
        place_id = data.get('place_id')
        name = data.get('name')
        address = data.get('address')

        if place_id and name:
            # Check if the restaurant already exists in the database
            restaurant, created = Restaurant.objects.get_or_create(
                place_id=place_id,
                defaults={'name': name, 'address': address}
            )

            # Check if the favorite already exists for this user
            favorite_exists = Favorite.objects.filter(user=request.user, restaurant=restaurant).exists()
            if favorite_exists:
                return JsonResponse({'status': 'exists'})

            # Create a new favorite
            Favorite.objects.create(user=request.user, restaurant=restaurant)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def map(request):
    favorites = []
    if request.user.is_authenticated:
        favorites = list(request.user.favorites.values_list('restaurant__place_id', flat=True))
    else:
        favorites = []

    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'favorites': json.dumps(favorites),
    }
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
@login_required
# ATLFoodFinder/views.py
@csrf_exempt
def save_favorite(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'unauthenticated'})

    if request.method == 'POST':
        data = json.loads(request.body)
        place_id = data.get('place_id')
        name = data.get('name')
        address = data.get('address')

        # Fetch photo_reference from Google Places API
        photo_reference = get_photo_reference(place_id)

        if place_id and name:
            restaurant, created = Restaurant.objects.get_or_create(
                place_id=place_id,
                defaults={'name': name, 'address': address, 'photo_reference': photo_reference}
            )
            # Update photo_reference if restaurant already exists
            if not created and not restaurant.photo_reference and photo_reference:
                restaurant.photo_reference = photo_reference
                restaurant.save()

            favorite_exists = Favorite.objects.filter(user=request.user, restaurant=restaurant).exists()
            if favorite_exists:
                return JsonResponse({'status': 'exists'})

            Favorite.objects.create(user=request.user, restaurant=restaurant)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

import requests
def get_photo_reference(place_id):
    api_key = settings.GOOGLE_MAPS_API_KEY
    url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=photo&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'result' in data and 'photos' in data['result']:
            photo_reference = data['result']['photos'][0]['photo_reference']
            return photo_reference
    return None
@csrf_exempt
@login_required
def delete_favorite(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        favorite_id = data.get('favorite_id')

        try:
            favorite = Favorite.objects.get(id=favorite_id, user=request.user)
            favorite.delete()
            return JsonResponse({'status': 'success'})
        except Favorite.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Favorite not found'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

