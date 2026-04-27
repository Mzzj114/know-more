"""
URL configuration for know_more project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

from django.views.i18n import JavaScriptCatalog
from django.contrib.sitemaps.views import sitemap
from sitemap import StaticViewSitemap, DocSitemap, ForumPostSitemap, CategorySitemap

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

# Sitemap configuration
sitemaps = {
    'static': StaticViewSitemap,
    'docs': DocSitemap,
    'forum_posts': ForumPostSitemap,
    'categories': CategorySitemap,
}

urlpatterns += [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

urlpatterns += i18n_patterns(
    path('know-more-admin/', admin.site.urls),
    path('docs/', include('docs.urls')),
    path('forum/', include('forum.urls', namespace='forum')),
    path('ai/', include('ai.urls')),
    path('auth/', include('account.urls')),
    path('', include('main.urls')),
    prefix_default_language=True,
)
