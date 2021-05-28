from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^login/$', views.login, name="login"),
    url(r'^authenticate/$', views.authenticate, name='authenticate'),
    url(r'^allworkflow/$', views.allworkflow, name='allworkflow'),
    url(r'^submitsql/$', views.submitSql, name='submitSql'),

]