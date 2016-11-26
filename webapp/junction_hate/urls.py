from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from rest_framework.reverse import reverse


from apps.text_api.views import ping, twitter_status, facebook_posts, facebook_comments, facebook_reactions, \
    nltk_analysis, analysis_page, wot_checking


class HybridRouter(routers.DefaultRouter):
    def __init__(self, *args, **kwargs):
        super(HybridRouter, self).__init__(*args, **kwargs)
        self.view_urls = []

    def add_url(self, view):
        self.view_urls.append(view)

    def get_urls(self):
        return super(HybridRouter, self).get_urls() + self.view_urls

    def get_api_root_view(self, **kwargs):
        original_view = super(HybridRouter, self).get_api_root_view()

        def view(request, *args, **kwargs):
            resp = original_view(request, *args, **kwargs)
            namespace = request.resolver_match.namespace
            for view_url in self.view_urls:
                name = view_url.name
                url_name = name
                if namespace:
                    url_name = namespace + ':' + url_name
                resp.data[name] = reverse(url_name,
                                          args=args,
                                          kwargs=kwargs,
                                          request=request,
                                          format=kwargs.get('format', None))
            return resp

        return view


router = HybridRouter(trailing_slash=False)

router.view_urls = [
    url(r'^ping', ping, name="Ping"),
    url(r'^twitter_status', twitter_status, name="Twitter status"),
    url(r'^facebook_comments', facebook_comments, name="Facebook_comments"),
    url(r'^facebook_reactions', facebook_reactions, name="Facebook reactions"),
    url(r'^facebook_posts', facebook_posts, name="Facebook posts"),
    url(r'^nltk_analysis', nltk_analysis, name="Nltk Analysis"),
    url(r'^wot_checking', wot_checking, name="WoT checking")
]

urlpatterns = [
    # utilities
    url(r'^admin/', admin.site.urls),

    # API
    url(r'^api/', include(router.urls)),
    url(r'^', include('rest_framework_docs.urls')),
    url(r'analysis$', analysis_page, name="analysis page")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
