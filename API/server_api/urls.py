from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PostView, CalliView
post_list = PostView.as_view({
    'post': 'create',
    'get': 'list'
})
post_detail = PostView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
calli_list = CalliView.as_view({
    'post': 'create',
    'get': 'list'
})
calli_detail = CalliView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
urlpatterns = format_suffix_patterns([
    path('auth', include('rest_framework.urls', namespace='rest_framework')),
    path('posts', post_list, name='post_list'),
    path('callis', calli_list, name='calli_list'),
    path('posts/<int:pk>/', post_detail, name='post_detail'),
    path('callis/<int:pk>/', calli_detail, name='calli_detail'),
])