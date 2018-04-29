from django.urls import path

from . import views

app_name = 'crm'
urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('<int:customer_id>/', views.customer_detail, name='detail'),
    path('<int:customer_id>/delete', views.delete, name='delete'),
    path('<int:customer_id>/update', views.update, name='update'),
]