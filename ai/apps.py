from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class AiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai'
    
    def ready(self):
        """应用启动时初始化调度器"""
        # 避免在 manage.py 命令中启动调度器
        import sys
        if 'runserver' in sys.argv or 'uwsgi' in sys.argv or 'gunicorn' in sys.argv:
            try:
                from .tasks import setup_scheduler
                setup_scheduler()
            except Exception as e:
                logger.error(f"启动调度器失败: {e}", exc_info=True)
