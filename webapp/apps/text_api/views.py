import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from apps.classifiers.HateBaseClassifier import HateBaseClassifier
from apps.classifiers.NltkClassifier import NltkClassifier
from apps.classifiers.WotChecker import WotChecker
from apps.text_interface import TextFromFacebook as Facebook
from apps.text_interface import TextFromTwitter as Twitter


@api_view()
def ping(request):
    return Response({'success': 'pong'}, status=200)


@api_view()
def twitter_status(request):
    """
    Return a list of twitter status for a user

    query params:
    - user: name of the page
    - number: nb of results (max=20)
    """
    user = request.query_params.get("user")
    nb = request.query_params.get("number")
    txt = Twitter.TextFromTwitter()
    list_tweets = txt.get_status_from_user(user=user, tweet_number=nb)
    return Response({"tweets": list_tweets}, status=200)


@api_view()
def facebook_posts(request):
    """
    Return a list of facebook posts

    query params:
    - name: name of the page
    - number: nb of results (max=20)
    """
    nb = request.query_params.get("number")
    name = request.query_params.get("page_name")
    fb = Facebook.TextFromFacebook()
    list_posts = fb.get_posts_from_page(page_name=name, post_number=nb)
    return Response({"posts": list_posts}, status=200)


@api_view()
def facebook_comments(request: Request):
    """
    Return a list of facebook comments for a post

    query params:
    - id: id of the post
    - number: nb of results (max=20)
    """

    nb = request.query_params.get("number")
    id = request.query_params.get("id")

    fb = Facebook.TextFromFacebook()
    list_comments = fb.get_comments_from_post(post_id=id, comment_number=nb)
    return Response({"comments": list_comments},
                    status=200)


@api_view()
def facebook_reactions(request, format=None):
    """
    Return a list of facebook reactions for a post

    query params:
    - id: id of the post
    """
    id = request.query_params.get("id")
    fb = Facebook.TextFromFacebook()
    reactions = fb.get_reactions_from_post(post_id=id)
    return Response({"reactions": reactions}, status=200)


@api_view()
def nltk_analysis(request):
    """
    query params:
    - text: text to analyze
    result: {
        'reactions': {
            'compound': between -1 and 1,
            'neg': between 0 and 1,
            'neu': between 0 and 1,
            'pos': between 0 and 1
        }
    }
    """
    nltk = NltkClassifier()
    text = request.query_params.get("text")
    analysis = nltk.analyse_text(text)
    return Response({"reactions": analysis}, status=200)


@api_view()
def wot_checking(request):
    """
    Query Web of Trust API for given websites

    Query params:
     - hosts: URLs of at most 100 host separated by '/' and ending by '/'

    Response: A list of Json objects following the schema below (one for each successful request)
    {
        'target': string (the URL host),
        'negative': Boolean,
        'undefined': Boolean,
        'positive': Boolean,
        'categories': {
            'malware': Boolean,
            'phishing': Boolean,
            'scam': Boolean,
            'potentially_illegal': Boolean,
            'misleading_or_unethical': Boolean,
            'privacy_risk': Boolean,
            'suspicious': Boolean,
            'hate': Boolean,
            'spam': Boolean,
            'pup': Boolean,
        }
    }
    """
    wot_checker = WotChecker()
    hosts = request.query_params.get("hosts")
    results = wot_checker.test_websites_concatenated(hosts)

    return Response({"results": results}, status=200)


def text_analysis_page(request):
    nltk = NltkClassifier()

    text = request.GET.get('text')
    if not text:
        return JsonResponse({"error": "please provide text"})

    analysis = nltk.analyse_text(text)

    hate_classifier = HateBaseClassifier()
    bad_words = hate_classifier.classify_with_info(text)

    arr, keys = [], []
    for (key, item) in analysis.items():
        arr.append(item)
        keys.append(key)

    return render(request, 'analysis/text_analysis.html',
                  {
                      "text": text,
                      "analysis": arr,
                      "keys_analysis": mark_safe(keys),
                      "bad_words": bad_words
                  })


def social_analysis(request):
    nltk = NltkClassifier()

    text = request.GET.get('text')
    if not text:
        return JsonResponse({"error": "please provide text"})

    analysis = nltk.analyse_text(text)

    arr, keys = [], []
    for (key, item) in analysis.items():
        arr.append(item)
        keys.append(key)

    return render(request, 'analysis/social_analysis.html',
                  {
                      "twitter": "",
                      "facebook": "",
                      "analysis": arr,
                      "keys_analysis": mark_safe(keys),
                  })
