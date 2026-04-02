from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from forum.models import Category, Post, Reply


class Command(BaseCommand):
    help = '初始化论坛测试数据'

    def handle(self, *args, **kwargs):
        self.stdout.write('开始创建测试数据...')
        
        # 创建分类
        categories_data = [
            {'name': '提示词工程', 'slug': 'prompt-engineering', 'description': '分享和讨论 AI 提示词技巧'},
            {'name': '学习路线案例', 'slug': 'learning-path', 'description': '使用 AI 设计学习路线的案例'},
            {'name': '技术交流', 'slug': 'tech-discussion', 'description': '技术交流和问答'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[category.slug] = category
            if created:
                self.stdout.write(f'✓ 创建分类：{category.name}')
        
        # 创建测试用户
        test_users = ['user1', 'user2', 'user3']
        users = {}
        
        for username in test_users:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'password': 'pbkdf2_sha256$600000$dummy_hash_for_testing'
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'✓ 创建测试用户：{username} (密码：password123)')
            users[username] = user
        
        # 创建测试帖子
        posts_data = [
            {
                'title': '如何写好系统提示词？',
                'content': '''大家好！我想请教一下关于系统提示词（System Prompt）的写作技巧。

我知道系统提示词对于控制 LLM 的行为非常重要，但是不知道应该如何组织语言和结构。

有没有什么最佳实践可以分享？

谢谢！''',
                'category_slug': 'prompt-engineering',
                'author_username': 'user1',
            },
            {
                'title': '使用 Meta-Prompting 设计 Python 学习路线',
                'content': '''我最近尝试使用 Meta-Prompting 技术来让 AI 帮我设计一份 Python 学习路线。

具体做法是：先让 AI 生成一个提示词模板，然后用这个模板来指导它输出更结构化的内容。

效果非常好！下面是我的实践过程...

## 第一步：设计元提示词

"你是一位经验丰富的 Python 开发者，请帮我设计一个提示词，用于引导 AI 为初学者制定 Python 学习计划"...

## 第二步：使用生成的提示词

[这里放实际的学习路线]

大家觉得这个方法怎么样？''',
                'category_slug': 'learning-path',
                'author_username': 'user2',
            },
            {
                'title': 'Django 论坛项目实战',
                'content': '''最近在用 Django 做一个论坛项目，记录一下开发过程中的要点：

### 技术栈选择
- 后端：Django 4.2
- 前端：Vue 3 + Element Plus
- 数据库：MySQL

### 核心功能
1. 发帖、回帖
2. 点赞、收藏
3. 用户系统
4. 后台管理

有感兴趣的朋友可以一起交流！''',
                'category_slug': 'tech-discussion',
                'author_username': 'user3',
            },
        ]
        
        for post_data in posts_data:
            category = categories[post_data['category_slug']]
            author = users[post_data['author_username']]
            
            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'content': post_data['content'],
                    'author': author,
                    'category': category,
                }
            )
            
            if created:
                self.stdout.write(f'✓ 创建帖子：{post.title}')
        
        self.stdout.write(self.style.SUCCESS('\n测试数据创建完成！'))
        self.stdout.write(self.style.WARNING('\n提示：'))
        self.stdout.write('- 测试用户：user1, user2, user3')
        self.stdout.write('- 默认密码：password123')
        self.stdout.write('- 超级用户：admin')
