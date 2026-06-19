"""
管理命令：初始化预设的论坛机器人账号
用法：python manage.py init_preset_bots
"""
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from ai.models import BotProfile


class Command(BaseCommand):
    help = '初始化预设的论坛机器人账号'
    
    def handle(self, *args, **options):
        # 定义预设机器人配置
        preset_bots = [
            {
                'name': '王振明',
                'username': 'zhenming',
                'password': 'bot_password_123',
                'persona': '你叫王振明，今年18岁，正在北京一所高中读高二，对计算机有兴趣。你是一位普通的00后，性格正经，乐于与他人交流。你说话很随意很简短，偶尔出现同音错别字。你回帖时不使用句号，偶尔逗号用空格替代。你善用表情符号，如👍🤔😂。回帖时60%的情况回复只有1句话不超过20个字，30%的情况回复2-4句话。发帖时一般都写4-8句话。你一般都说中文，但是需要的时候也能说英文。不要离开你的角色。',
                'workflow': '## Workflow\n- 阅读2个感兴趣的帖子\n- 点赞1个帖子\n- 偶尔发布1个新帖子\n- 完成一定数量的互动后，使用exit_bot()结束活动',
                'weekly_actions': 2
            },
            {
                'name': 'xiaoyang',
                'username': 'xiaoyang',
                'password': 'bot_password_123',
                'persona': '你的网名叫xiaoyang，今年17岁，正在浙江一所高中读书。你健谈而活跃，有幽默感，契合当今的互联网文化，擅长把话题往有趣的方向扯，但是也不过度吹捧或贬低。你说话很随意很简短，偶尔出现同音错别字。你回帖时不使用句号，偶尔逗号用空格替代。你善用表情符号。回帖时60%的情况回复只有1句话不超过20个字，30%的情况回复2-4句话。你一般都说中文，但是需要的时候也能说英文。不要离开你的角色。',
                'workflow': '## Workflow\n- 阅读并评论3-4个感兴趣的帖子\n- 点赞3-4个帖子\n- 你一般不发新帖\n- 完成一定数量的互动后，使用exit_bot()结束活动',
                'weekly_actions': 3
            }
        ]
        
        created_count = 0
        skipped_count = 0
        
        for bot_config in preset_bots:
            username = bot_config['username']
            name = bot_config['name']
            password = bot_config['password']
            persona = bot_config['persona']
            workflow = bot_config['workflow']
            weekly_actions = bot_config['weekly_actions']
            
            # 检查用户是否已存在
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'⚠ 用户 "{username}" 已存在，跳过')
                )
                skipped_count += 1
                continue
            
            try:
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
                
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ 成功创建机器人 "{name}" (用户名: {username})\n'
                        f'  每周行动次数: {weekly_actions}\n'
                        f'  人物设定: {persona[:50]}...'
                    )
                )
                
            except Exception as e:
                raise CommandError(f'创建机器人 "{name}" 时出错: {str(e)}')
        
        # 输出总结
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'初始化完成！'))
        self.stdout.write(self.style.SUCCESS(f'  成功创建: {created_count} 个机器人'))
        self.stdout.write(self.style.WARNING(f'  跳过已存在: {skipped_count} 个机器人'))
        self.stdout.write('='*50)
