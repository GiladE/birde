from django.conf.urls import patterns, include, url
from django.contrib import admin

from birde import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'birde.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
)
