#
# Copyright 2019 IBM Corp. All Rights Reserved.
# Licensed under the Apache License, Version 2.0
# 
# Author: Erika Agostinelli

# INSTRUCTION:
# Copy and paste this code in your Cloud Function and make sure to add your 
# Twitter Dev Account Credential in the code -> Save  
# Then create a default parameter for 'account' variable by sing the "Parameters" tab on the left
# menu to test if the function works (use Invoke)
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
# 
#

import sys
import requests 
import base64

def main(dict):
    """
    Function that allows to send a get request to twitter API and retrieve the last 3 tweets of a 
    specific account name. The parameter of the account is passed by Watson Assistant throught a 
    context variable. 

    Args: 
        dict (dict): containing the parameter - in our case only one is used : "account" (e.g. @blackmirror)
    Return: 
        list_tweets (list) : list containing text (and image) of the last three tweets. 
    """

    account_name = dict.get("account")[1:]
    
    client_key = '// your twitter dev account client_key //'
    client_secret = '// your twitter dev account client_secret //'

    key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')

    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)

    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }


    auth_data = {
        'grant_type': 'client_credentials'
    }

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)

    access_token = auth_resp.json()['access_token']
    
    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)    
    }

    search_url = '{}1.1/statuses/user_timeline.json?screen_name={}&count=3'.format(base_url, account_name)
    search_resp = requests.get(search_url, headers=search_headers)
    tweet_data = search_resp.json()

    list_tweets =[]
    
    for i in range(len(tweet_data)): 
        # store the text of the tweet 
        text = tweet_data[i].get("text")

        # if the tweet contains an image add this to the tweet text
        if(tweet_data[i].get("entities").get("media")):
            image = tweet_data[i].get("entities").get("media")[0].get("media_url_https")
            width = tweet_data[i].get("entities").get("media")[0].get("sizes").get("small").get("w")
            height = tweet_data[i].get("entities").get("media")[0].get("sizes").get("small").get("h")
            url = tweet_data[i].get("entities").get("media")[0].get("url")
            final = text + "<a href = '" + url + "'>" + "<img src = '" +image + "' height =" + str(height) + " width = "+ str(width) + ">" + "</a>"
            list_tweets.append(final)
        # if there is no image, then just save the text of the tweet 
        else:
            list_tweets.append(text)
        
    return {"result": list_tweets}