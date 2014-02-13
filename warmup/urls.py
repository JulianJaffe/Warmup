from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'warmup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^users/', include('users.urls'), name='users'),
    url(r'^TESTAPI/', include('users.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
