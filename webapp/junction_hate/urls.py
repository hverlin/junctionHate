from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    # utilities
    url(r'^admin/', admin.site.urls),

    # API
    url(r'^', include(router.urls)),

    # url(r'^docs/', include('rest_framework_docs.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
