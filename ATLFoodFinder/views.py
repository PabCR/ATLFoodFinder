from django.shortcuts import render

def home(request):
    return render(request, 'ATLFoodFinder/home.html')