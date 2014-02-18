from django.conf.urls import patterns, include, url

from django.contrib import admin, auth
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'warmup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'(?i)^users/', include('users.urls'), name='users'),
    url(r'(?i)^TESTAPI/', include('users.urls'), name='testapi'),
    url(r'(?i)^client/', include('users.urls', namespace='client')),
    url(r'(?i)^admin/', include(admin.site.urls), name='admin'),
)
