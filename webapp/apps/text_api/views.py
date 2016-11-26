from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from apps.classifiers.NltkClassifier import NltkClassifier
from apps.text_interface import TextFromFacebook as Facebook
from apps.text_interface import TextFromTwitter as Twitter
from apps.fact_checker import DuckduckgoSearch as DuckSearch
from apps.fact_checker import WebSiteCredibility


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
    """
    nltk = NltkClassifier()
    text = request.query_params.get("text")
    analysis = nltk.analyse_text(text)
    return Response({"reactions": analysis}, status=200)



@api_view()
def search_score(request, format=None):
    """
    Return a score compute in function of the websites get by a duckduckgo research

    query params:
    - search: search string
    """
    search = request.query_params.get("search")
    website_liste = DuckSearch.search_on_html_duckduckgo(search=search)
    score = WebSiteCredibility.compute_score_for_website_liste(website_list=website_liste)
    return Response({"search": search,"score": score}, status=200)
