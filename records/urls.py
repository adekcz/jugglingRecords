from django.conf.urls import url
from django.conf.urls import include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profilePage/(\w*)', views.profilePage, name='profilePage'),
    url(r'^recordCategoryPage/(\w*)-(\w*)-(\w*)', views.recordCategoryPage, name='recordCategoryPage'),
    url(r'^loginPage', views.loginPage, name='loginPage'),
    #url('^', include('django.contrib.auth.urls')),
 url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^register/$', views.registration, name='register'),
    ]
