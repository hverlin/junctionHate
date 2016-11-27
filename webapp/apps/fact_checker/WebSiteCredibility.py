from apps.text_api.models import Site
from apps.text_api.models import WebsiteType
from urllib.parse import urlparse


def compute_score_for_website_liste(website_list):
    scores = dict()
    types = dict()
    for type in WebsiteType.objects.all():
        scores[type.name] = 0
        types[type.id] = type.name

    for website in website_list:
        #get just the start of url whitout www.
        url = urlparse(website)
        netloc = url.netloc.replace("www.", "")

        q = Site.objects.filter(url__icontains=netloc)
        for res in q:
            type = types[res.type_id]
            scores[type] += 1

    return scores