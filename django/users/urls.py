from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('<int:user_selected_id>/', views.user_detail, name='detail'),
    path('<int:user_selected_id>/delete', views.delete, name='delete'),
    path('<int:user_selected_id>/update', views.update, name='update'),
]