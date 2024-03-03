from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogDetailView, BlogListView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('create/', BlogCreateView.as_view(), name='create'),
    path('', BlogListView.as_view(), name='list'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blogs'),
]
