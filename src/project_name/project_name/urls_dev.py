
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from {{ project_name }}.urls import urlpatterns, patterns, url

urlpatterns += staticfiles_urlpatterns() + patterns(
    '', url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    'document_root': settings.MEDIA_ROOT}))
