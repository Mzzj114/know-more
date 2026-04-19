import json
import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from .forms import CustomUserCreationForm

def send_verify_code(request):
    """
    发送邮箱验证码 API
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': _('仅支持 POST 请求')})
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
    except Exception:
        email = request.POST.get('email')
        
    if not email:
        return JsonResponse({'success': False, 'message': _('缺少邮箱地址')})
        
    if User.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'message': _('该邮箱已被注册')})

    # 简单的频率限制防刷 (60 秒)
    if cache.get(f"verify_lock_{email}"):
        return JsonResponse({'success': False, 'message': _('验证码发送太频繁，请稍后再试')})

    code = f"{random.randint(100000, 999999)}"
    
    # 存入 Cache，有效期 5 分钟 (300秒)
    cache.set(f"verify_code_{email}", code, 300)
    # 防刷锁，有效期 60 秒
    cache.set(f"verify_lock_{email}", "locked", 60)

    try:
        send_mail(
            subject=_('Know More 注册验证码'),
            message=_('欢迎注册 Know More。您的注册验证码是：%(code)s，请在 5 分钟内完成输入。如非本人操作，请忽略此邮件。') % {'code': code},
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        return JsonResponse({'success': False, 'message': _('发送邮件失败: %(error)s') % {'error': str(e)}})

    return JsonResponse({'success': True, 'message': _('验证码已发送')})


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
                form.add_error(None, _("请输入验证码"))
            else:
                cached_code = cache.get(f"verify_code_{email}")
                if not cached_code:
                    form.add_error(None, _("验证码已过期或不存在，请重新发送"))
                elif str(cached_code) != str(input_code):
                    form.add_error(None, _("验证码错误"))
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

def send_reset_code(request):
    """
    发送重置密码的邮箱验证码 API
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': _('仅支持 POST 请求')})
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
    except Exception:
        email = request.POST.get('email')
        
    if not email:
        return JsonResponse({'success': False, 'message': _('缺少邮箱地址')})
        
    if not User.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'message': _('该邮箱未注册账号')})

    # 简单的频率限制防刷 (60 秒)
    if cache.get(f"reset_lock_{email}"):
        return JsonResponse({'success': False, 'message': _('验证码发送太频繁，请稍后再试')})

    code = f"{random.randint(100000, 999999)}"
    
    cache.set(f"reset_code_{email}", code, 300)
    cache.set(f"reset_lock_{email}", "locked", 60)

    try:
        send_mail(
            subject=_('Know More 重置密码验证码'),
            message=_('您正在申请修改密码。您的验证码是：%(code)s，请在 5 分钟内完成输入。如非本人操作，请密切关注您的账号安全。') % {'code': code},
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        return JsonResponse({'success': False, 'message': _('发送邮件失败: %(error)s') % {'error': str(e)}})

    return JsonResponse({'success': True, 'message': _('验证码已发送')})

def reset_password(request):
    """
    修改/重置密码视图
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        input_code = request.POST.get('verification_code')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        error_msg = None
        if not email or not input_code or not password or not confirm_password:
            error_msg = _("请填写所有必填字段")
        elif password != confirm_password:
            error_msg = _("两次输入的密码不一致")
        else:
            cached_code = cache.get(f"reset_code_{email}")
            if not cached_code:
                error_msg = _("验证码已过期或不存在，请重新发送")
            elif str(cached_code) != str(input_code):
                error_msg = _("验证码错误")
            else:
                user = User.objects.filter(email=email).first()
                if not user:
                    error_msg = _("系统中找不到该邮箱对应的用户")
                else:
                    # 验证成功，执行密码重置
                    user.set_password(password)
                    user.save()
                    cache.delete(f"reset_code_{email}")
                    cache.delete(f"reset_lock_{email}")
                    
                    # 保持已有会话并且不需要踢人下线
                    update_session_auth_hash(request, user)
                    
                    if request.user.is_authenticated:
                        # 已经是登录状态，回修改前所在的主页或主站
                        return redirect('user_profile')
                    else:
                        # 未登录状态，要求回到登录页
                        return redirect('login')
        
        return render(request, 'auth/reset_password.html', {'error_msg': error_msg, 'email': email})

    # GET 端回显已有的绑定邮箱保障逻辑（若登录则只读回显）
    initial_email = request.user.email if request.user.is_authenticated else ""
    return render(request, 'auth/reset_password.html', {'email': initial_email})
