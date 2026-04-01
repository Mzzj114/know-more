from django.shortcuts import render


def home(request):
    """
    主页视图 — 纯前端展示，无后端逻辑。
    传递 nav_active 标记以控制导航栏的高亮状态。
    """
    return render(request, 'main/home.html', {
        'nav_active': 'home',
    })
