import random
import requests
import hmac
import hashlib
import base64
import time
import json
import logging
from datetime import datetime
from urllib.parse import quote
from collections import deque

# Setup logging
logging.basicConfig(level=logging.INFO)

# Amazon Product Advertising API credentials
ACCESS_KEY = 'YOUR_ACCESS_KEY'
SECRET_KEY = 'YOUR_SECRET_KEY'
PARTNER_TAG = 'YOUR_PARTNER_TAG'
MARKETPLACE = 'webservices.amazon.com'  # Change this based on the marketplace you are targeting

# Base URL for Product Advertising API
BASE_URL = f"https://{MARKETPLACE}/paapi5/searchitems"

# History of past choices
history = deque(maxlen=10)

def create_signature(secret_key, date, region, service, string_to_sign):
    """
    Create the signature required for Amazon Product Advertising API
    """
    kDate = hmac.new(("AWS4" + secret_key).encode('utf-8'), date.encode('utf-8'), hashlib.sha256).digest()
    kRegion = hmac.new(kDate, region.encode('utf-8'), hashlib.sha256).digest()
    kService = hmac.new(kRegion, service.encode('utf-8'), hashlib.sha256).digest()
    kSigning = hmac.new(kService, 'aws4_request'.encode('utf-8'), hashlib.sha256).digest()
    return hmac.new(kSigning, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

def get_amazon_recommendations(keywords):
    """
    Search for items on Amazon using keywords
    """
    # Payload for the API request
    payload = json.dumps({
        "Keywords": keywords,
        "Resources": ["ItemInfo.Title", "Offers.Listings.Price", "Offers.Listings.Availability", "CustomerReviews.StarRating", "CustomerReviews.Count"],
        "PartnerTag": PARTNER_TAG,
        "PartnerType": "Associates",
        "Marketplace": "www.amazon.com"
    })
    
    # Create the canonical request
    current_time = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    payload_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    canonical_request = f'POST\n/paapi5/searchitems\n\nhost:{MARKETPLACE}\nx-amz-date:{current_time}\nx-amz-target:com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems\n{payload_hash}'
    
    # Create the string to sign
    string_to_sign = f'AWS4-HMAC-SHA256\n{current_time}\n{current_time[:8]}/us-east-1/ProductAdvertisingAPI/aws4_request\n{hashlib.sha256(canonical_request.encode()).hexdigest()}'
    
    # Create the signature
    signature = create_signature(SECRET_KEY, current_time[:8], 'us-east-1', 'ProductAdvertisingAPI', string_to_sign)
    
    # Create the authorization header
    authorization_header = f'AWS4-HMAC-SHA256 Credential={ACCESS_KEY}/{current_time[:8]}/us-east-1/ProductAdvertisingAPI/aws4_request, SignedHeaders=host;x-amz-date;x-amz-target, Signature={signature}'
    
    # Headers for the API request
    headers = {
        'Content-Type': 'application/json',
        'X-Amz-Target': 'com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems',
                'Host': MARKETPLACE,
        'X-Amz-Date': current_time,
        'Authorization': authorization_header
    }
    
    # Make the API request
    response = requests.post(BASE_URL, headers=headers, data=payload)
    
    # Handle rate limits and errors
    if response.status_code == 429:
        logging.warning("Rate limit exceeded. Waiting for 1 minute.")
        time.sleep(60)
        return get_amazon_recommendations(keywords)
    elif response.status_code != 200:
        logging.error(f"Error: {response.status_code} - {response.text}")
        return None
    
    # Parse the response
    return parse_response(response.json())

def parse_response(response):
    """
    Parse the response from the Amazon Product Advertising API
    """
    try:
        items = response.get('SearchResult', {}).get('Items', [])
        recommendations = []
        for item in items:
            title = item.get('ItemInfo', {}).get('Title', {}).get('DisplayValue', '')
            price = item.get('Offers', {}).get('Listings', [{}])[0].get('Price', {}).get('Amount', '')
            availability = item.get('Offers', {}).get('Listings', [{}])[0].get('Availability', {}).get('Message', '')
            rating = item.get('CustomerReviews', {}).get('StarRating', {}).get('Rated', '')
            review_count = item.get('CustomerReviews', {}).get('Count', '')
            recommendations.append({'title': title, 'price': price, 'availability': availability, 'rating': rating, 'review_count': review_count})
        return recommendations
    except Exception as e:
        logging.error(f"Error parsing response: {e}")
        return []

def make_decision(options):
    """
    This function takes a list of options and selects the one with the highest rating.
    If multiple options have the same rating, it selects the one with the lowest price.
    """
    if not options:
        logging.error("No options provided")
        return {'error': 'No options provided', 'status_code': 400}
    
    # Sort by rating, review count, and price
    options.sort(key=lambda x: (-float(x.get('rating', 0)), int(x.get('review_count', 0)), float(x.get('price', float('inf')))))
    
    # Select the top option that hasn't been selected recently
    for option in options:
        if option['title'] not in history:
            history.append(option['title'])
            return option
    
    # If all options have been selected recently, just return the top option
    return options[0]

# Example usage:
try:
    category = "chocolate snacks"
    recommendations = get_amazon_recommendations(category)

    if recommendations:
        decision = make_decision(recommendations)
        print(f"Recommended product: {decision['title']}, Price: {decision['price']}, Availability: {decision['availability']}, Rating: {decision['rating']}, Review Count: {decision['review_count']}")
    else:
        print("No recommendations available.")
except Exception as e:
    logging.error(f"An error occurred: {e}")
