import requests

def get_data_from_api(url):
    """Fetches data from a given URL using an external API call."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API call failed: {e}")
        return None

def process_data(url):
    data = get_data_from_api(url)
    if data:
        return f"Processed: {data.get('status', 'unknown')}"
    return "No data to process"
