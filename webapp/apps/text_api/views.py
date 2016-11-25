from django.http import JsonResponse
from apps.text_interface import TextFromTwitter as twitter
from apps.text_interface import TextFromFacebook as facebook


def ping(request):
    return JsonResponse({'success': 'pong'}, status=200)


def twitter_status(request):
    txt = twitter.TextFromTwitter()
    list_tweets = txt.get_status_from_user(user="abcd", tweet_number=10)
    return JsonResponse({"tweets": list_tweets}, status=200)


def facebook_posts(request):
    fb = facebook.TextFromFacebook()
    list_posts = fb.get_posts_from_page(page_name="DonaldTrump", post_number=10)
    return JsonResponse({"posts": list_posts}, status=200)
