"""portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from posts.views import getMe, getVisualArt, index, art, getArtsFromCategory, getBlogHome, getBlogPost, getThumbnail
from posts.views import getPostsFromCategory
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('visualart/<str:artID>/', getVisualArt),
    path('thumbnail/<str:artID>/', getThumbnail),
    path('', index),
    path('about/', getMe),
    path('art/<str:artID>/', art),
    path('category/<str:categoryID>/', getArtsFromCategory),
    path('blog/', getBlogHome),
    path('post/<str:postID>/', getBlogPost),
    path('blogcategory/<str:categoryID>/', getPostsFromCategory)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
