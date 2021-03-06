"""epic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from main import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="home"),
    path('articles/<str:name>/',views.detail_article,name="article_detail"),
    path('auth/articles/create',views.article_create,name="article_create"),
    path("auth/articles/view",views.get_articles,name="get_artcle"),
    path("auth/articles/callback/remove/<int:id>",views.RemoveArticleView,name='remove_article')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

