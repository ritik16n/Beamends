from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

from hello import views

from django.contrib.auth import views as auth_views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^db', views.db, name='db'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^hello/',include('hello.urls')),
    
]
