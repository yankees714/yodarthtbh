from twython import Twython, TwythonStreamer
import requests

from settings import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET
from settings import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
from settings import YO_TOKEN


class UserStreamer(TwythonStreamer):
    def __init__(self, screen_name, consumer_key, consumer_secret, access_token, access_token_secret):
        super(UserStreamer, self).__init__(consumer_key, consumer_secret, access_token, access_token_secret)
        self.screen_name = screen_name

    def on_success(self, data):
        if "text" in data and "user" in data:
            tweet = data["text"].encode("utf-8")
            user = data["user"]["screen_name"].encode("utf-8")
            if self.screen_name == user:
                print user
                print tweet
                if "tbh" in tweet:
                    response = yo_all(YO_TOKEN, "https://twitter.com/darth")
                    print response,"yo!"

    def on_error(self, status_code, data):
        print status_code
        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        self.disconnect()


def yo_all(api_token, link):
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