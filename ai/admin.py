from django.contrib import admin
from .models import UserTokenUsage

@admin.register(UserTokenUsage)
class UserTokenUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'remaining_tokens', 'last_reset_date')
    search_fields = ('user__username', 'user__email')
    list_filter = ('last_reset_date',)
