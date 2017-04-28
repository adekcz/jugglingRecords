"""url mapper with root in /records"""
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [ #pylint: disable=invalid-name
    url(r'^$', views.index, name='index'),
    url(r'^index-(\w+)$', views.index, name='index-prop'),
    url(r'^profilePage/([\w\.\@]*)', views.profile_page, name='profilePage'),
    url(r'^recordCategoryPage/(\w*)-(\w*)-([ \w]*)',
        views.record_category_page, name='recordCategoryPage'),
    url(r'^loginPage', views.login_page, name='loginPage'),
    #url('^', include('django.contrib.auth.urls')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^register/$', views.registration, name='register'),
    url(r'^newRecord/$', views.new_entry, name='newRecord'),
    url(r'^newRecord/(?P<category_id>\d+)/$', views.new_entry, name='newRecord'),
    url(r'^editRecord/(\d+)$', views.edit_entry, name='editRecord'),
    url(r'^showRecord/(\d+)$', views.edit_entry, name='showRecord'),
    url(r'^showRecord/$', views.edit_entry, name='showRecord'),
    url(r'^newCategory/$', views.new_category, name='newCategory'),
    url(r'^accountSettings/$', views.account_settings, name='accountSettings'),
    url(r'^deleteRecord/(?P<pk>\d+)/$', views.RecordDelete.as_view(), name='entry_delete'),
    ]
