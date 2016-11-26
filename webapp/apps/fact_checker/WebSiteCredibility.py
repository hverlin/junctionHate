from apps.text_api.models import Site
from urllib.parse import urlparse


def compute_score_for_website_liste(website_list):
    score = 0

    for website in website_list:
        url = urlparse(website)
        netloc = url.netloc.replace("www.", "")

        print(netloc)
        q = Site.objects.filter(url__icontains=netloc)
        #print(q)

    return score