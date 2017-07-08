from django.conf.urls import url
import views

urlpatterns=[
    url(r'^register/$',views.register),
    url(r'^register_headle/$', views.register_headle),
    url(r'^login/$', views.login),
    url(r'^login_headle/$', views.login_headle),
    url(r'^loginout/$',views.loginout),
    url(r'^$',views.center),
    url(r'^order/$',views.order),
    url(r'^site/$',views.site),


]