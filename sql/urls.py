from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.allworkflow, name='allworkflow'),
    url(r'^index/$', views.allworkflow, name='allworkflow'),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^authenticate/$', views.authenticate, name='authenticate'),
    url(r'^allworkflow/$', views.allworkflow, name='allworkflow'),
    url(r'^submitsql/$', views.submitSql, name='submitSql'),

    url(r'^autoreview/$', views.autoreview, name='autoreview'),
    url(r'^detail/$', views.detail, name='detail'),
    url(r'^rollback/$', views.rollback, name='rollback'),
]