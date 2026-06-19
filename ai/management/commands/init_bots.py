"""
管理命令：初始化论坛机器人账号
用法：python manage.py init_bots
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ai.models import BotProfile


class Command(BaseCommand):
    help = '初始化论坛机器人账号'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--name',
            type=str,
            help='机器人名称',
            required=True
        )
        parser.add_argument(
            '--username',
            type=str,
            help='机器人用户名',
            required=True
        )
        parser.add_argument(
            '--password',
            type=str,
            help='机器人密码（默认: bot_password_123）',
            default='bot_password_123'
        )
        parser.add_argument(
            '--persona',
            type=str,
            help='人物设定提示词',
            required=True
        )
        parser.add_argument(
            '--workflow',
            type=str,
            help='工作流程提示词',
            default=''
        )
        parser.add_argument(
            '--weekly-actions',
            type=int,
            help='每周行动次数（默认: 3）',
            default=3
        )
    
    def handle(self, *args, **options):
        username = options['username']
        name = options['name']
        password = options['password']
        persona = options['persona']
        workflow = options['workflow']
        weekly_actions = options['weekly_actions']
        
        # 检查用户是否已存在
        if User.objects.filter(username=username).exists():
            raise CommandError(f'用户 "{username}" 已存在')
        
        # 创建用户
        user = User.objects.create_user(
            username=username,
            password=password,
            is_active=True
        )
        
        # 创建机器人档案
        bot_profile = BotProfile.objects.create(
            user=user,
            name=name,
            persona_prompt=persona,
            workflow_prompt=workflow,
            is_active=True,
            weekly_action_count=weekly_actions
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✓ 成功创建机器人 "{name}" (用户名: {username})\n'
                f'  每周行动次数: {weekly_actions}\n'
                f'  人物设定: {persona[:50]}...'
            )
        )
