from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profilePage/(\w*)', views.profilePage, name='profilePage'),
]
