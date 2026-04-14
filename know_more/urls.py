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
from django.conf.urls.i18n import i18n_patterns, set_language
from main import views

# Non-i18n URLs (no language prefix)
urlpatterns = [
    path('admin/', admin.site.urls),
    # Root path - auto redirect to language-specific docs
    path('', views.root_redirect, name='root_redirect'),
    path('i18n/setlang/', set_language, name='set_language'),
]

# i18n URLs (with language prefix)
urlpatterns += i18n_patterns(
    path('docs/', include('docs.urls')),
    path('forum/', include('forum.urls', namespace='forum')),
    path('ai/', include('ai.urls')),
    path('auth/', include('account.urls')),
    path('', include('main.urls')),
    prefix_default_language=True,  # All languages require prefix
)
