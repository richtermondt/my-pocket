import requests
import json
import os


class PocketClient:
    def __init__(self, consumer_key, redirect_uri='https://example.com'):
        self.consumer_key = consumer_key
        self.redirect_uri = redirect_uri
        self.access_token = self.load_access_token()
        self.base_url = "https://getpocket.com/v3/get"
        self.headers = {'X-Accept': 'application/json'}

    def load_access_token(self):
        """Load access token from a file, if it exists."""
        if os.path.exists("access_token.json"):
            with open("access_token.json", "r") as file:
                data = json.load(file)
                return data.get("access_token")
        return None

    def save_access_token(self, access_token):
        """Save access token to a file."""
        with open("access_token.json", "w") as file:
            json.dump({"access_token": access_token}, file)

    def get_request_token(self):
        """Obtain a request token from Pocket."""
        url = "https://getpocket.com/v3/oauth/request"
        headers = {'X-Accept': 'application/json'}
        data = {
            'consumer_key': self.consumer_key,
            'redirect_uri': self.redirect_uri
        }
        response = requests.post(url, headers=headers, data=data)
        response_data = response.json()
        return response_data['code']

    def authorize_app(self, request_token):
        """Generate the authorization URL for the user to authorize the app."""
        auth_url = f"https://getpocket.com/auth/authorize?request_token={
            request_token}&redirect_uri={self.redirect_uri}"
        print(
            f"Please go to the following URL and authorize the app: {auth_url}")
        input("Once you have authorized the app, press Enter to continue...")

    def get_access_token(self, request_token):
        """Convert the request token into an access token."""
        url = "https://getpocket.com/v3/oauth/authorize"
        headers = {'X-Accept': 'application/json'}
        data = {
            'consumer_key': self.consumer_key,
            'code': request_token
        }
        response = requests.post(url, headers=headers, data=data)
        response_data = response.json()
        return response_data['access_token']

    def authenticate(self):
        """Handle the complete OAuth flow to obtain an access token for the first time."""
        if self.access_token is None:
            request_token = self.get_request_token()
            self.authorize_app(request_token)
            self.access_token = self.get_access_token(request_token)
            self.save_access_token(self.access_token)
            print("Access token obtained and saved.")

    def retrieve(self, state=None, favorite=None, tag=None, content_type=None, sort=None, detail_type=None, search=None,
                 domain=None, since=None, count=None, offset=None):
        """Retrieve items from Pocket with various options."""
        self.authenticate()  # Ensure the user is authenticated before making requests

        data = {
            'consumer_key': self.consumer_key,
            'access_token': self.access_token,
        }

        # Optional parameters
        if state:
            data['state'] = state
        if favorite:
            data['favorite'] = favorite
        if tag:
            data['tag'] = tag
        if content_type:
            data['contentType'] = content_type
        if sort:
            data['sort'] = sort
        if detail_type:
            data['detailType'] = detail_type
        if search:
            data['search'] = search
        if domain:
            data['domain'] = domain
        if since:
            data['since'] = since
        if count:
            data['count'] = count
        if offset:
            data['offset'] = offset

        response = requests.post(
            self.base_url, headers=self.headers, data=data)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()


# Example usage:
if __name__ == "__main__":
    # Replace with your actual consumer_key
    CONSUMER_KEY = os.getenv('POCKET_CONSUMER_KEY')

    pocket_client = PocketClient(CONSUMER_KEY)

    # Retrieve 5 unread items, sorted by newest, with full details
    items = pocket_client.retrieve(
        state='unread', count=5, sort='newest', detail_type='complete')

    # Print retrieved items
    for item_id, item_details in items['list'].items():
        print(f"Item ID: {item_id}")
        print(f"Title: {item_details.get('resolved_title')}")
        print(f"URL: {item_details.get('resolved_url')}")
        print()
