import pandas as pd
import requests
import os

def get_request_token(consumer_key):
    url = 'https://getpocket.com/v3/oauth/request'
    headers = {"Content-Type" : "application/json; charset=UTF-8", "X-Accept" : "application/json"}
    data = {'consumer_key': consumer_key, 'redirect_uri':'https://techleaderinsights.com'}
    pocket_api = requests.post(url, headers=headers, json=data)
    
    return pocket_api.json()["code"]


def get_access_token(consumer_key, request_token):
    url = 'https://getpocket.com/v3/oauth/authorize' # Set destination URL here
    headers = {"Content-Type" : "application/json; charset=UTF-8", "X-Accept" : "application/json"}
    data = {"consumer_key":consumer_key,"code":request_token}
    pocket_api = requests.post(url, headers=headers, json=data)
    return pocket_api.json()["access_token"]

# step 3  GET request for data in JSON format
def get_data(consumer_key, access_token):
    parameters = {"consumer_key":consumer_key,"access_token":access_token, "count" : "10"}
    pocket_api = requests.get("https://getpocket.com/v3/get", params=parameters)
    return pocket_api

def get_pandas_df(response):
    return pd.DataFrame(response.json()['list'])

def transpose_df(data_frame):
   return data_frame.transpose()

def main():

    consumer_key = os.getenv('POCKET_CONSUMER_KEY')

    request_token = get_request_token(consumer_key)
    auth_url = "https://getpocket.com/auth/authorize?request_token=" + request_token + "&redirect_uri=pocketapp1234:authorizationFinished"

    print("Authorize request request by navigating to url:")
    print(auth_url)

    message = input("Have you authorized request?")

    if message.upper().startswith("Y"):

    # Step 3: get access token code=4f19f11a-a156-b301-75b1-255691
        access_key = get_access_token(consumer_key, request_token)

        response = get_data(consumer_key, access_key)

        # do some things with pandas??
        df = get_pandas_df(response)

        print(df)
        tdf = transpose_df(df)
        print(tdf)
    
    print("Exit......")

main()








