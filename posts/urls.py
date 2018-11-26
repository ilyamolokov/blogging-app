from django.urls import path
from . import views

app_name='posts'

urlpatterns= [
    path('', views.posts_list, name="list"),
    path('create/', views.posts_create, name='create'),
    path('drafts/', views.posts_drafts, name='posts_drafts'),
    path('<int:id>/', views.posts_detail, name="posts_detail"),
    path('<int:id>/update/', views.posts_update, name="update"),
    path('<int:id>/delete/', views.posts_delete, name='delete'),

]
