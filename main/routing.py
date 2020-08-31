# Websocket protocol handler

from . import consumers
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/articles/', consumers.ArticleConsumer,name='article_update'),
    re_path(r'ws/posts/\w+/$',consumers.ArticleDetailConsumer,name='article_detail')
]