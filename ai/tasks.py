"""
论坛机器人任务调度
使用 APScheduler 触发，django-q2 异步执行
"""
import random
import logging
from datetime import datetime, timedelta
from django.utils import timezone
from django_q.tasks import schedule
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.contrib.auth.models import User
from .models import BotProfile

logger = logging.getLogger(__name__)


def generate_random_times_for_week(start_time, count_range=(1, 5)):
    """
    生成本周内的随机时间点
    
    Args:
        start_time: 本周起始时间（周一8:00）
        count_range: 行动次数范围 (min, max)
    
    Returns:
        datetime 列表
    """
    end_time = start_time + timedelta(weeks=1)  # 下周一8:00
    total_seconds = int((end_time - start_time).total_seconds())
    
    # 随机选择行动次数
    count = random.randint(count_range[0], count_range[1])
    
    random_times = []
    for _ in range(count):
        random_offset = random.randint(0, total_seconds)
        random_times.append(start_time + timedelta(seconds=random_offset))
    
    # 去重并排序
    random_times = sorted(list(set(random_times)))
    
    return random_times


def schedule_bot_actions():
    """
    为所有激活的机器人生成本周的行动计划并提交到 django-q2
    由 APScheduler 每周一8点触发
    """
    logger.info("开始为机器人安排本周行动...")
    
    # 获取所有激活的机器人
    active_bots = BotProfile.objects.filter(is_active=True).select_related('user')
    
    if not active_bots.exists():
        logger.info("没有激活的机器人，跳过")
        return
    
    # 计算本周一8:00
    now = timezone.now()
    days_since_monday = now.weekday()
    this_monday = now.date() - timedelta(days=days_since_monday)
    start_time = datetime.combine(this_monday, datetime.min.time()) + timedelta(hours=8)
    start_time = timezone.make_aware(start_time)
    
    for bot_profile in active_bots:
        bot_user = bot_profile.user
        
        # 为该机器人生成随机行动时间
        action_times = generate_random_times_for_week(
            start_time, 
            count_range=(1, bot_profile.weekly_action_count)
        )
        
        logger.info(f"机器人 '{bot_profile.name}' 将执行 {len(action_times)} 次行动:")
        
        for i, action_time in enumerate(action_times, 1):
            # 提交到 django-q2 队列
            schedule(
                'ai.bot_engine.execute_bot_action',
                bot_user.id,  # 传递用户ID作为参数
                name=f'bot_{bot_profile.id}_{action_time.strftime("%Y%m%d_%H%M%S")}_{i}',
                schedule_type='O',  # ONCE
                next_run=action_time,
                repeats=1,
                group=f'bot_{bot_profile.id}',
                timeout=300  # 5分钟超时
            )
            
            logger.info(f"  时间点 {i}: {action_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    logger.info(f"✓ 任务安排完成！共 {active_bots.count()} 个机器人")


def setup_scheduler():
    """
    设置 APScheduler 调度器
    在 Django 启动时调用
    """
    scheduler = BackgroundScheduler()
    
    # 添加定时任务：每周一上午8点执行 schedule_bot_actions
    scheduler.add_job(
        func=schedule_bot_actions,
        trigger=CronTrigger(day_of_week='mon', hour=8, minute=0),
        id='weekly_bot_schedule_trigger',
        name='每周机器人行动触发器',
        replace_existing=True
    )
    
    # 启动调度器
    scheduler.start()
    
    logger.info("APScheduler 已启动")
    
    return scheduler
