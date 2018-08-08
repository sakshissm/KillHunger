from django.conf.urls import url
from . import views
app_name='app'

urlpatterns=[
  url(r'^register/$',views.register,name='register'),
  url(r'^login/$',views.user_login,name='user_login'),
  url(r'^logout/$',views.user_logout,name='user_logout'),
  url(r'^apply/$',views.apply,name='apply'),
  url(r'^area/$',views.area,name='area'),
  url(r'^(?P<pk>\d+)/donate/$', views.donate, name='donate'),
  url(r'^(?P<pk>\d+)/status/$', views.change_status, name='status'),
  url(r'^(?P<pk>\d+)/contact/$',views.contact,name='contact'),
  url(r'^$',views.index,name='index'),

]
