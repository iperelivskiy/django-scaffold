
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from {{ project_name }}.urls import urlpatterns


urlpatterns += staticfiles_urlpatterns() + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
