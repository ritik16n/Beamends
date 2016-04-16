from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

from app1 import views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^db', views.db, name='db'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('allauth.urls')),

    url(r'^app1/',include('app1.urls')),

    url(r'^accounts/login/$',auth_views.login,{'template_name':'allauth/account/login.html'},name='login'),

    url(r'^accounts/logout/$',auth_views.logout,{'template_name':'app1/base.html'},name='logout'),

    url(r'^accounts/password_change/$',auth_views.password_change,{'template_name':'app1/registration/password_change.html'},name='password_change'),

    url(r'^accounts/password_change/done/$',auth_views.password_change_done,{'template_name':'app1/userprofile/saved.html'},name='password_change_done'),

    url(r'^accounts/password_reset/$',auth_views.password_reset,{'template_name':'app1/registration/password_reset_form.html'},name='password_reset'),

    url(r'^accounts/password_reset/done/$',auth_views.password_reset_done,{'template_name':'app1/registration/password_reset_done.html'},name='password_reset_done'),

    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.password_reset_confirm,{'template_name':'app1/registration/password_reset_confirm.html'},name='password_reset_confirm'),

    url(r'^accounts/reset/done/$',auth_views.password_reset_complete,{'template_name':'app1/registration/password_reset_complete'},name='password_reset_complete'),

]
