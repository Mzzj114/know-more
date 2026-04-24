from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from forum.models import Post, Category
from docs.utils import get_all_docs


class StaticViewSitemap(Sitemap):
    """静态页面站点地图"""
    
    def items(self):
        return ['home', 'doc_index', 'forum:forum_index']
    
    def location(self, item):
        return reverse(item)
    
    def changefreq(self, item):
        if item == 'home':
            return 'weekly'
        elif item == 'doc_index':
            return 'monthly'
        elif item == 'forum:forum_index':
            return 'daily'
        return 'monthly'
    
    def priority(self, item):
        if item == 'home':
            return 1.0
        elif item == 'doc_index':
            return 0.8
        elif item == 'forum:forum_index':
            return 0.7
        return 0.5


class DocSitemap(Sitemap):
    """文档站点地图"""
    
    changefreq = "monthly"
    priority = 0.6
    
    def items(self):
        return get_all_docs()
    
    def location(self, obj):
        return f"/docs/{obj['slug']}/"


class ForumPostSitemap(Sitemap):
    """论坛帖子站点地图"""
    
    changefreq = "daily"
    priority = 0.5
    
    def items(self):
        return Post.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return f"/forum/post/{obj.pk}/"


class CategorySitemap(Sitemap):
    """论坛分类站点地图"""
    
    changefreq = "weekly"
    priority = 0.6
    
    def items(self):
        return Category.objects.all()
    
    def location(self, obj):
        return f"/forum/category/{obj.slug}/"