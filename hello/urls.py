from django.conf.urls import include, url
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[

    url(r'^register/$',views.register,name='register'),

    url(r'^add/(?P<user_id>[0-9]+)/$',views.add,name='add'),

    url(r'^prehome/$',views.prehome,name='prehome'),

    url(r'^homepage/(?P<user_id>[0-9]+)/$',views.homepage,name='homepage'),

    url(r'^error/$',views.error,name='error'),

    url(r'^log/(?P<user_pk>[0-9]+)/$',views.log,name='log'),

    url(r'^displayform/(?P<user_pk>[0-9]+)/$',views.displayform,name='displayform'),

    url(r'^editform/(?P<user_pk>[0-9]+)/$',views.editform,name='editform'),

    url(r'^foredit/(?P<d_id>[0-9]+)/(?P<user_id>[0-9]+)/$',views.edit,name='edit'),

    url(r'^deleteform/(?P<user_id>[0-9]+)/$',views.deleteform,name='deleteform'),

    url(r'^deletedone/(?P<d_id>[0-9]+)/(?P<user_id>[0-9]+)/$',views.delete,name='delete'),

    url(r'^fromandto/(?P<user_pk>[0-9]+)/$',views.fromandto,name='fromandto'),

    url(r'^settings/(?P<user_pk>[0-9]+)/$',views.settings,name='settings'),

    url(r'^changeuserform/(?P<user_pk>[0-9]+)/$',views.changeuserform,name='changeuserform'),

    url(r'^changeemailform/(?P<user_pk>[0-9]+)/$',views.changeemailform,name='changeemailform'),

    url(r'^saved/$',views.saved,name='saved'),

    url(r'^generatecsv/(?P<user_id>[0-9]+)/$',views.generatecsv,name='generatecsv'),

    #url(r'^userprofile/renderchart/(?P<user_id>[0-9]+)/$',views.renderchart,name='renderchart'),

]
