from django.urls import path
from . import views 
#from .feeds import LatestPostFeed

app_name = 'blog'

urlpatterns=[
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('tags/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('create/', views.postCreate, name='create_post'),
    path('edit/<int:post_id>/', views.postEdit, name='edit_post'),
    path('my-articles/', views.InstructorPosts, name='instructor_posts'),
    path('delete/<int:post_id>/', views.postDelete, name='delete_post'),
    #path('feed/', LatestPostFeed(), name="post_feed"),
    path('search/', views.post_search, name='post_search'),
]