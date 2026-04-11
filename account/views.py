import json
import random
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.cache import cache
from django.core.mail import send_mail
from .forms import CustomUserCreationForm

def send_verify_code(request):
    """
    发送邮箱验证码 API
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': '仅支持 POST 请求'})
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
    except Exception:
        email = request.POST.get('email')
        
    if not email:
        return JsonResponse({'success': False, 'message': '缺少邮箱地址'})
        
    if User.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'message': '该邮箱已被注册'})

    # 简单的频率限制防刷 (60 秒)
    if cache.get(f"verify_lock_{email}"):
        return JsonResponse({'success': False, 'message': '验证码发送太频繁，请稍后再试'})

    code = f"{random.randint(100000, 999999)}"
    
    # 存入 Cache，有效期 5 分钟 (300秒)
    cache.set(f"verify_code_{email}", code, 300)
    # 防刷锁，有效期 60 秒
    cache.set(f"verify_lock_{email}", "locked", 60)

    try:
        send_mail(
            subject='Know More 注册验证码',
            message=f'欢迎注册 Know More。您的注册验证码是：{code}，请在 5 分钟内完成输入。如非本人操作，请忽略此邮件。',
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'发送邮件失败: {str(e)}'})

    return JsonResponse({'success': True, 'message': '验证码已发送'})


def register(request):
    """
    用户注册视图
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            input_code = request.POST.get('verification_code')
            
            if not input_code:
                form.add_error(None, "请输入验证码")
            else:
                cached_code = cache.get(f"verify_code_{email}")
                if not cached_code:
                    form.add_error(None, "验证码已过期或不存在，请重新发送")
                elif str(cached_code) != str(input_code):
                    form.add_error(None, "验证码错误")
                else:
                    # 验证成功
                    user = form.save()
                    cache.delete(f"verify_code_{email}")
                    cache.delete(f"verify_lock_{email}")
                    login(request, user)
                    return redirect('user_profile')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'auth/register.html', {'form': form})
