"""
Module to hold different types of search request handlers.
"""

import json
import oauth2 as oauth
import socket
import urllib
import urllib.request as request

from django.conf import settings
from parallel_run import constants

# timeout in seconds
timeout = 1
socket.setdefaulttimeout(timeout)


class BaseHandler(object):

    handler = None

    def __init__(self, q):
        self.q = q
        self.url = constants.URLS[self.handler]

    def request(self, url):
        """
        Methdo to fire GET requests witht he given url.

        :param url: The actual URL that needs to be fired.
        """
        response = request.urlopen(url)
        return json.loads(response.read().decode("utf-8"))
        
    def fire(self):
        """
        Method to trigger api request.
        """
        url = self.generate_uri()
        response = {
            self.handler: {
                "url": url,
            }
        }

        try:
           data = self.format(self.request(url))
        except urllib.error.URLError as e:
            response[self.handler].update({
                "error": "Request timeout",
                "__parallelfail": True
            })
        except Exception as e:
            response[self.handler].update({
                "error": "No data found",
                "__parallelfail": True
            })
        else:
            response[self.handler].update({
                "text": data
            })

        return response


class Google(BaseHandler):

    handler = "google"
    
    def generate_uri(self):
        """generate uri method"""
        return self.url.format(q=self.q, key=settings.GOOGLE_CLIENT_KEY)

    def format(self, data):
        """
        Method to format the GOOGLE response.
        """
        items = data.get("items")
        if items and isinstance(items, list) and len(items):
            data = items[0]["snippet"]
            return data
        else:
            return "No results found"


class DuckDuckGo(BaseHandler):

    handler = "duckduckgo"

    def generate_uri(self):
        """generate uri method"""
        return self.url.format(q=self.q)

    def format(self, data):
        """
        Method to format the GOOGLE response.
        """
        items = data.get("RelatedTopics")
        if items and isinstance(items, list) and len(items):
            data = items[0]["Text"]
            return data
        else:
            return "No results found"


class Twitter(BaseHandler):

    handler = "twitter"
    
    def generate_uri(self):
        """
        Method to make the url.
        """
        consumer = oauth.Consumer(
            key=settings.CONSUMER_KEY,
            secret=settings.CONSUMER_SECRET
        )
        token = oauth.Token(
            key=settings.TOKEN_KEY,
            secret=settings.TOKEN_SECRET
        )

        req = oauth.Request.from_consumer_and_token(
            consumer,
            token=token,
            http_method="GET",
            http_url=self.url,
            parameters=None,
            body=b"",
            is_form_encoded=False
        )
        req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), consumer, token)

        return req.to_url()

    def format(self, data):
        """
        Method to format the response content.

        :param data: json response received.
        """
        items = data.get("statuses")
        if items and isinstance(items, list) and len(items):
            data = items[0]["user"]["description"]
            return data
        else:
            return "No results found"
