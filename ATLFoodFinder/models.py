# ATLFoodFinder/models.py
from django.db import models
from django.contrib.auth.models import User

# ATLFoodFinder/models.py

class Restaurant(models.Model):
    place_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    photo_reference = models.CharField(max_length=500, blank=True, null=True) 

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant')  # Prevent duplicate favorites

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.restaurant.name}"

