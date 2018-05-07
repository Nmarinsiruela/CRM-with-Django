from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/create$', views.UserCreate.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^customers/$', views.CustomerList.as_view()),
    url(r'^customers/create$', views.CustomerCreate.as_view()),
    url(r'^customers/(?P<pk>[0-9]+)/$', views.CustomerDetail.as_view()),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)