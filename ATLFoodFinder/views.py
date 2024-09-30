from django.http import JsonResponse
from django.shortcuts import render
from .services import get_embed_map_url, get_filtered_restaurants
import os

def home(request):
    return render(request, 'ATLFoodFinder/home.html')

def show_map_view(request):
    location = request.GET.get('location', 'Atlanta, GA')  # Default location is Atlanta
    embed_map_url = get_embed_map_url(location)
    return render(request, 'map_display.html', {'map_url': embed_map_url})

def map_view(request):
    google_maps_key = os.getenv('GOOGLE_MAPS_KEY')
    return render(request, 'map.html', {'google_maps_key': google_maps_key})

def restaurant_list_view(request):
    """
    View to fetch and display filtered restaurant data based on user input.
    """
    # Get the city and optional cuisine filter from the query parameters
    city = request.GET.get('city', 'Atlanta')  # Default city is 'Atlanta'
    cuisine = request.GET.get('cuisine', None)  # Optional cuisine filter

    # Fetch the filtered restaurant data using the Google Places API
    restaurants = get_filtered_restaurants(city, cuisine)

    # Pass the filtered data to the template for rendering
    return render(request, 'restaurant_list.html', {'restaurants': restaurants, 'city': city, 'cuisine': cuisine})


def get_restaurants_view(request):
    """
    View to handle API requests for fetching filtered restaurant data.
    """
    # Extract query parameters from the request
    city = request.GET.get('city', 'Atlanta')  # Default to Atlanta if no city provided
    cuisine = request.GET.get('cuisine', None)  # Cuisine filter, optional

    # Use the service function to get filtered restaurant data
    restaurants = get_filtered_restaurants(city, cuisine)

    # Return the list of restaurants as JSON
    return JsonResponse({'restaurants': restaurants})


def get_embed_map_view(request):
    """
    View to handle API requests for getting the Google Maps embed URL.
    """
    # Extract location from the request, default to Atlanta if not provided
    location = request.GET.get('location', 'Atlanta, GA')
    # Use the service function to generate the embed map URL
    embed_url = get_embed_map_url(location)
    # Return the embed map URL as JSON
    return JsonResponse({'embed_url': embed_url})

