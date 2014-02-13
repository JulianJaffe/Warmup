from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^adduser$', views.addUser, name='user'),
    url(r'^resetFixture$', views.resetFixture, name='reset'),
    url(r'^unitTests$', views.unitTests, name='test'),
)
