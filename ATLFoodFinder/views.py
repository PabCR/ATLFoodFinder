from django.shortcuts import render

def home(request):
    return render(request, 'ATLFoodFinder/home.html')

def map(request):
    return render(request, 'ATLFoodFinder/map.html')