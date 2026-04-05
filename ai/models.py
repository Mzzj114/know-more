from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserTokenUsage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ai_token_usage', verbose_name='用户')
    remaining_tokens = models.IntegerField(default=50000, verbose_name='剩余可用 Tokens')
    last_reset_date = models.DateField(default=timezone.now, verbose_name='上次重置日期')

    class Meta:
        verbose_name = '用户 Token 使用量'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user.username} 的 Token 容量'
