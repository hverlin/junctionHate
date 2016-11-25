import tweepy
from TextInterfaces.TextFrom import TextFrom


class TextFromTwitter(TextFrom):
    def __init__(self):
        consumer_key = 'VqLtcUiHKrWy8YXfgWODFyFoe'
        consumer_secret = '7YNxcOhtHRjpq1ybx6RRE28WId2028z6S2y69L3bN6rmJJggx1'
        access_token = '140961368-NSM1xsEFmgIcJre5doFnV50JtAc2JjBdI46GB0nf'
        access_token_secret = 'fykaXl80SYQrG3TbePVZAGmuT6zyrd8fQl0f3BLtwz2S2'

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth)

    def get_status_from_user(self, user, tweet_number=1):
        status = self.api.user_timeline(screen_name=user, count=tweet_number)
        for s in status:
            self.string_list.append(s.text)
        return self.string_list
