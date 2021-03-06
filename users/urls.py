from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
    url(r'(?i)^$', views.client),
    url(r'(?i)^count$', views.count, name='count'),
    url(r'(?i)^login$', views.login, name='login'),
    url(r'(?i)^add$', views.addUser, name='user'),
    url(r'(?i)^resetFixture$', views.resetFixture, name='reset'),
    url(r'(?i)^unitTests$', views.unitTests, name='test'),
)
