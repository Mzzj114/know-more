from django.contrib import admin
from .models import UserTokenUsage, BotProfile, BotActionLog

@admin.register(UserTokenUsage)
class UserTokenUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'remaining_tokens', 'last_reset_date')
    search_fields = ('user__username', 'user__email')
    list_filter = ('last_reset_date',)


@admin.register(BotProfile)
class BotProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_active', 'weekly_action_count', 'total_posts', 'total_replies', 'total_likes', 'last_action_at')
    search_fields = ('name', 'user__username')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('created_at', 'last_action_at', 'total_posts', 'total_replies', 'total_likes')


@admin.register(BotActionLog)
class BotActionLogAdmin(admin.ModelAdmin):
    list_display = ('bot', 'action_type', 'status', 'scheduled_at', 'executed_at')
    search_fields = ('bot__name', 'content_preview')
    list_filter = ('action_type', 'status', 'scheduled_at')
    readonly_fields = ('created_at', 'executed_at')
