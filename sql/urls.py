from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^test1/$', views.test1, name='test1'),
]