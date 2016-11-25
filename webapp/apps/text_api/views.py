from django.http import JsonResponse
from apps.text_interface import TextFromTwitter as twitter


def ping(request):
    return JsonResponse({'success': 'pong'}, status=200)


def twitter_status(request):
    txt = twitter.TextFromTwitter()
    list_tweets = txt.get_status_from_user(user="abcd", tweet_number=10)
    return JsonResponse({"tweets": list_tweets}, status=200)
