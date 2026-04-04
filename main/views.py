import os
import json
from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import render


def home(request):
    """
    主页视图 — 纯前端展示，无后端逻辑。
    传递 nav_active 标记以控制导航栏的高亮状态。
    """
    return render(request, 'main/home.html', {
        'nav_active': 'home',
    })

def tutorial_page(request, slug=None):
    """
    提示词教程视图 — 渲染页面骨架，由 Vue 负责加载和渲染具体内容。
    """
    return render(request, 'main/tutorial.html', {
        'nav_active': 'tutorial',
        'current_slug': slug,
    })

def get_tutorials_dir():
    return os.path.join(settings.BASE_DIR, 'static', 'tutorials')

def api_tutorial_list(request):
    """
    获取所有可用的教程列表 (用于渲染侧边栏目录)
    """
    tutorials_dir = get_tutorials_dir()
    tutorials = []
    
    if os.path.exists(tutorials_dir):
        for filename in os.listdir(tutorials_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(tutorials_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        slug = filename[:-5]  # 去除 .json 后缀
                        tutorials.append({
                            'slug': slug,
                            'title': data.get('title', slug)
                        })
                except Exception:
                    continue
                    
    return JsonResponse({'tutorials': tutorials})

def api_tutorial_detail(request, slug):
    """
    获取单个教程的详细 JSON 数据
    """
    if not slug or '..' in slug or '/' in slug or '\\' in slug:
        raise Http404("Invalid tutorial slug")
        
    tutorials_dir = get_tutorials_dir()
    filepath = os.path.join(tutorials_dir, f"{slug}.json")
    
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return JsonResponse(data)
        except Exception:
            raise Http404("Error reading tutorial data")
            
    raise Http404("Tutorial not found")
