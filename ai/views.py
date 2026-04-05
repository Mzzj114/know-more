import os
import json
import datetime
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
from .models import UserTokenUsage

def check_and_reset_session_tokens(request):
    now = timezone.now().date()
    last_reset = request.session.get('ai_last_reset_date')
    if last_reset:
        try:
            last_reset_date = datetime.date.fromisoformat(last_reset)
            if last_reset_date.isocalendar()[1] != now.isocalendar()[1] or last_reset_date.year != now.year:
                request.session['ai_remaining_tokens'] = 5000
                request.session['ai_last_reset_date'] = now.isoformat()
        except ValueError:
            request.session['ai_remaining_tokens'] = 5000
            request.session['ai_last_reset_date'] = now.isoformat()
    else:
        request.session['ai_remaining_tokens'] = 5000
        request.session['ai_last_reset_date'] = now.isoformat()
    return request.session.get('ai_remaining_tokens', 5000)

def check_and_reset_user_tokens(user):
    usage, created = UserTokenUsage.objects.get_or_create(user=user)
    now = timezone.now().date()
    if created or usage.last_reset_date.isocalendar()[1] != now.isocalendar()[1] or usage.last_reset_date.year != now.year:
        usage.remaining_tokens = 50000
        usage.last_reset_date = now
        usage.save()
    return usage

@csrf_exempt
def chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. Must be POST.'}, status=405)
    
    try:
        data = json.loads(request.body)
        messages = data.get('messages', [])
        model_name = data.get('model', 'gpt-3.5-turbo')
    except Exception:
        return JsonResponse({'error': 'Invalid JSON body.'}, status=400)
        
    if not messages:
        return JsonResponse({'error': 'No messages provided.'}, status=400)

    # 1. Resource check
    if request.user.is_authenticated:
        usage = check_and_reset_user_tokens(request.user)
        remaining = usage.remaining_tokens
    else:
        remaining = check_and_reset_session_tokens(request)

    if remaining <= 0:
        return JsonResponse({'error': 'Weekly token limit exceeded.'}, status=403)

    # 2. Call OpenAI
    api_key = os.environ.get('api_key')
    if not api_key:
        return JsonResponse({'error': 'Server configuration error (missing api_key).'}, status=500)

    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=502)

    # 3. Deduct tokens
    tokens_used = response.usage.total_tokens
    
    if request.user.is_authenticated:
        usage.remaining_tokens = max(0, usage.remaining_tokens - tokens_used)
        usage.save()
    else:
        request.session['ai_remaining_tokens'] = max(0, remaining - tokens_used)

    return JsonResponse({
        'content': response.choices[0].message.content,
        'tokens_used': tokens_used,
        'remaining_tokens': max(0, remaining - tokens_used)
    }, status=200)

