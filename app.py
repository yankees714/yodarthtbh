from twython import Twython, TwythonStreamer
import requests

from settings import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
from settings import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
from settings import YO_TOKEN


class UserStreamer(TwythonStreamer):
    """ Streams tweets from the given user, and sends a yo when a tweet includes 'tbh'. """
    def __init__(self, screen_name, consumer_key, consumer_secret, access_token, access_token_secret):
        super(UserStreamer, self).__init__(consumer_key, consumer_secret, access_token, access_token_secret)
        self.screen_name = screen_name

    def on_success(self, data):
        """ Handles a successfully retreived tweet. """
        if "text" in data and "user" in data and "id_str" in data:
            tweet = data["text"].encode("utf-8")
            user = data["user"]["screen_name"].encode("utf-8")
            tweet_id = data["id_str"].encode("utf-8")
            
            if user == self.screen_name:
                print user
                print tweet
                if "tbh" in tweet:
                    response = yo_all(YO_TOKEN, "https://twitter.com/"+self.screen_name+"/status/"+tweet_id)
                    print response,"yo!"

    def on_error(self, status_code, data):
        """ Handles an error with the streamer. """
        print status_code
        self.disconnect()   # Stop getting tweets


def yo_all(api_token, link):
    """ Sends a yo through the given token with the specified link attached. """
    return requests.post("http://api.justyo.co/yoall/", data={'api_token': api_token, 'link': link})


def main():
    HANDLE = "darth"

    # Look up user id for the target handle
    twitter = Twython(
        TWITTER_CONSUMER_KEY,
        TWITTER_CONSUMER_SECRET,
        TWITTER_ACCESS_TOKEN,
        TWITTER_ACCESS_TOKEN_SECRET
    )
    user_id = twitter.lookup_user(screen_name=HANDLE)[0]["id_str"]
    print "@"+HANDLE+",","id",user_id

    # Set up the user stream and follow it
    stream = UserStreamer(
        HANDLE,
        TWITTER_CONSUMER_KEY,
        TWITTER_CONSUMER_SECRET,
        TWITTER_ACCESS_TOKEN,
        TWITTER_ACCESS_TOKEN_SECRET
    )
    stream.statuses.filter(follow=user_id)


if __name__ == "__main__":
    main()
