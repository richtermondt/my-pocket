import json
import pandas as pd
import requests
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def get_request_token(consumer_key):
    url = 'https://getpocket.com/v3/oauth/request' # Set destination URL here
    post_fields = {"consumer_key":consumer_key,"redirect_uri":"http://www.google.com"}   # Set POST fields here
    request = Request(url, urlencode(post_fields).encode())
    json = urlopen(request).read().decode()
    return json



# request_token = "bc30dcf7-eec7-940d-48bb-303226"
# step 2 POST request an access token
def get_access_token(consumer_key, request_token):
    url = 'https://getpocket.com/v3/oauth/authorize' # Set destination URL here
    post_fields = {"consumer_key":consumer_key,"code":request_token}   # Set POST fields hereabspost_request = Request(url, urlencode(post_fields).encode())
    request = Request(url, urlencode(post_fields).encode())
    json = urlopen(request).read().decode()
    return json


# access_token=5a334a5e-9ff4-6a57-715e-9d9ae9&username=richtermondt



# step 3  GET request for data in JSON format
def get_data(consumer_key, access_token):
    parameters = {"consumer_key":consumer_key,"access_token":access_token}
    response = requests.get("https://getpocket.com/v3/get", params=parameters)
    print(response.json())
    return response

def get_pandas_df(response):
    return pd.DataFrame(response.json()['list'])

def transpose_df(data_frame):
   return data_frame.transpose()

def main():
    consumer_key = "93564-b211e77222b22d6ff9f6e078"

    # Step 1: get request token
    #request_token = get_request_token(consumer_key)
    #print(request_token)

    # Step 2: Authorize app - you will need to:
    # 1 - construct a url with the request token
    # 2 Use browser to navigate to the url - haven't figured out how to get by this limitation
    # e.g. - https://getpocket.com/auth/authorize?request_token=your_request_token&redirect_uri=http://www.google.com

    # Step 3: get access token code=4f19f11a-a156-b301-75b1-255691
    # access_key = get_access_token(consumer_key, "ed069bfb-7119-d73c-3368-2601ec")
    # print(access_key)

    # Step 4: Start making api requests!!
    access_key = "5a334a5e-9ff4-6a57-715e-9d9ae9"
    response = get_data(consumer_key, access_key)

    # print(response)

    # do some things with pandas??
    # df = get_pandas_df(response)
    # tdf = transpose_df(df)

main()








