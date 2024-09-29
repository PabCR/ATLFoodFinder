import requests
from django.conf import settings


def get_embed_map_url(location):
    """
    Generates a Google Maps Embed API URL for a given location.

    Args:
    - location (str): Location can be an address (e.g., "Atlanta, GA") or coordinates (e.g., "33.7490,-84.3880").
    
    Returns:
    - str: A URL for embedding an interactive Google Map.
    """
    base_url = "https://www.google.com/maps/embed/v1/place"
    
    # Access your API key from the settings
    api_key = settings.GOOGLE_MAPS_API_KEY

    # Prepare the URL with the location and API key
    embed_url = f"{base_url}?q={location}&key={api_key}"

    return embed_url


def get_filtered_restaurants(city, cuisine=None):
    """
    Fetch and filter restaurant data from Google Places API based on city and optional cuisine filter.

    Args:
    - city (str): The city to search for restaurants.
    - cuisine (str, optional): Filter by cuisine type (e.g., 'Italian').

    Returns:
    - list: A list of filtered restaurant data from the Google Places API.
    """
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    api_key = settings.GOOGLE_MAPS_KEY

    # Create the search query for restaurants in the given city
    query = f"restaurants in {city}"
    if cuisine:
        query += f" {cuisine}"

    # Set up the query parameters for the API request
    params = {
        "query": query,
        "key": api_key,
    }

    try:
        # Make a request to the Google Places API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an error for bad responses

        # Return the list of restaurants from the API response
        return response.json().get('results', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching restaurant data: {e}")
        return []
