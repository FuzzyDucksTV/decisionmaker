import requests
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Set up logging
logging.basicConfig(level=logging.ERROR)

def fetch_data_from_api(api_url, params=None, headers=None, auth=None):
    """
    Fetch data from a third-party API.
    
    :param api_url: The URL of the API endpoint.
    :param params: Optional dictionary of query parameters to be sent with the request.
    :param headers: Optional dictionary of headers to be sent with the request.
    :param auth: Optional authentication tuple or object to send with the request.
    :return: The response data as a JSON object.
    """
    try:
        # Set up rate limiting and retries
        session = requests.Session()
        retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        # Send a GET request to the API
        response = session.get(api_url, params=params, headers=headers, auth=auth)
        
        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            # Parse the response JSON and return it
            return response.json()
        else:
            # If the status code is not 200, raise an exception
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Log any errors that occur during the request
        logging.error(f"An error occurred: {e}")
        return None

# Example usage:
api_url = "https://api.example.com/data"
params = {"param1": "value1", "param2": "value2"}
headers = {"Authorization": "Bearer YOUR_ACCESS_TOKEN"}
auth = ("username", "password")

# Fetch data from the API
data = fetch_data_from_api(api_url, params, headers, auth)

# Output the data
print(data)
