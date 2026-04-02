from django.apps import AppConfig


class ForumConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forum'
    
    def ready(self):
        """导入信号处理器"""
        import forum.signals  # noqa