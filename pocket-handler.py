import os
import requests

# Step 1: Get your consumer_key from the Pocket Developer Portal
CONSUMER_KEY = os.getenv('POCKET_CONSUMER_KEY')

# Step 2: Obtain a request token
def get_request_token(consumer_key):
    url = "https://getpocket.com/v3/oauth/request"
    headers = {'X-Accept': 'application/json'}
    data = {'consumer_key': consumer_key, 'redirect_uri': 'https://example.com'}
    
    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()
    return response_data['code']

# Step 3: Redirect the user to Pocket to authorize your app
def authorize_app(request_token):
    auth_url = f"https://getpocket.com/auth/authorize?request_token={request_token}&redirect_uri=https://example.com"
    print(f"Please go to the following URL and authorize the app: {auth_url}")

# Step 4: Convert the request token into an access token
def get_access_token(consumer_key, request_token):
    try:
        url = "https://getpocket.com/v3/oauth/authorize"
        headers = {'X-Accept': 'application/json'}
        data = {'consumer_key': consumer_key, 'code': request_token}

        response = requests.post(url, headers=headers, data=data)
        
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            response_data = response.json()
            return response_data['access_token']
        else:
            print("Error: Failed to retrieve access token")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}")
        return None

# Step 5: Retrieve saved items
def get_saved_items(consumer_key, access_token):
    url = "https://getpocket.com/v3/get"
    headers = {'X-Accept': 'application/json'}
    data = {
        'consumer_key': consumer_key,
        'access_token': access_token,
        'count': 10,  # Number of items to retrieve
        'detailType': 'complete'  # Include full details
    }
    
    response = requests.post(url, headers=headers, data=data)
    return response.json()

def get_article_details(consumer_key, access_token, item_id):
    url = "https://getpocket.com/v3/get"
    headers = {'X-Accept': 'application/json'}
    data = {
        'consumer_key': consumer_key,
        'access_token': access_token,
        'item_id': item_id,
        'detailType': 'complete'  # Include full details
    }
    
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# Example Usage
if __name__ == "__main__":
    # Get request token
    request_token = get_request_token(CONSUMER_KEY)
    
    # Authorize app (this will output a URL you need to visit in your browser)
    authorize_app(request_token)
    
    input("Once you have completed the authorization in your browser, press Enter to continue...")
   
    # Once authorized, convert the request token to an access token
    access_token = get_access_token(CONSUMER_KEY, request_token)
    
    # Retrieve saved items from Pocket
    saved_items = get_saved_items(CONSUMER_KEY, access_token)
    
    # Print the retrieved items
    for item_id, item_details in saved_items['list'].items():
        print(f"Item ID: {item_id}")
        print(f"Title: {item_details.get('resolved_title')}")
        print(f"URL: {item_details.get('resolved_url')}")
        print()