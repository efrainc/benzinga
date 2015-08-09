from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^transaction/', views.trans, name='transaction'),
    url(r'^sell/$', views.trans, name='transaction'),
    url(r'^thanks/$', views.thanks, name='thanks'),
    url(r'^whoops/$', views.whoops, name='whoops'),
]
