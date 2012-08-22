# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
	url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)