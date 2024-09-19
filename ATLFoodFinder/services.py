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