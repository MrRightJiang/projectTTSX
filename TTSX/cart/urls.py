from django.conf.urls import url
import views

urlpatterns=[
    url(r'^add/$',views.add),
    url(r'^count/$', views.count),
    url(r'^index/',views.index),
    url(r'^del/$',views.delete),
    url(r'^edit/$', views.edit),
    url(r'^order/$',views.order)
]