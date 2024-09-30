from django.shortcuts import render
from .services import get_embed_map_url


def home(request):
    return render(request, 'ATLFoodFinder/home.html')

def show_map_view(request):
    location = request.GET.get('location', 'Atlanta, GA')  # Default location is Atlanta
    embed_map_url = get_embed_map_url(location)
    
    return render(request, 'map_display.html', {'map_url': embed_map_url})
def map(request):
    return render(request, 'ATLFoodFinder/map.html')
def favorites(request):
    return render(request, 'ATLFoodFinder/favorites.html')

