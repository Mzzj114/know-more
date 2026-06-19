"""
论坛机器人功能测试脚本
用于快速验证所有组件是否正确安装和配置
"""
import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'know_more.settings.dev')
django.setup()

def test_imports():
    """测试所有模块是否可以正常导入"""
    print("=" * 60)
    print("测试 1: 模块导入")
    print("=" * 60)
    
    try:
        from ai.models import BotProfile, BotActionLog
        print("✓ ai.models 导入成功")
    except Exception as e:
        print(f"✗ ai.models 导入失败: {e}")
        return False
    
    try:
        from ai.forum_tools import (
            exit_bot, add_to_favourite, like, reply, post, 
            read_post, get_forum_overview
        )
        print("✓ ai.forum_tools 导入成功")
    except Exception as e:
        print(f"✗ ai.forum_tools 导入失败: {e}")
        return False
    
    try:
        from ai.bot_engine import execute_bot_action, TOOLS
        print("✓ ai.bot_engine 导入成功")
        print(f"  - 工具数量: {len(TOOLS)}")
    except Exception as e:
        print(f"✗ ai.bot_engine 导入失败: {e}")
        return False
    
    try:
        from ai.tasks import schedule_bot_actions, setup_scheduler
        print("✓ ai.tasks 导入成功")
    except Exception as e:
        print(f"✗ ai.tasks 导入失败: {e}")
        return False
    
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        print("✓ APScheduler 导入成功")
    except Exception as e:
        print(f"✗ APScheduler 导入失败: {e}")
        return False
    
    try:
        from django_q.tasks import schedule
        print("✓ django-q2 导入成功")
    except Exception as e:
        print(f"✗ django-q2 导入失败: {e}")
        return False
    
    print()
    return True


def test_models():
    """测试模型是否正确创建"""
    print("=" * 60)
    print("测试 2: 数据库模型")
    print("=" * 60)
    
    try:
        from ai.models import BotProfile, BotActionLog
        
        # 检查表是否存在
        bot_count = BotProfile.objects.count()
        log_count = BotActionLog.objects.count()
        
        print(f"✓ BotProfile 表存在，当前记录数: {bot_count}")
        print(f"✓ BotActionLog 表存在，当前记录数: {log_count}")
        print()
        return True
    except Exception as e:
        print(f"✗ 模型测试失败: {e}")
        print()
        return False


def test_settings():
    """测试 Django 配置"""
    print("=" * 60)
    print("测试 3: Django 配置")
    print("=" * 60)
    
    from django.conf import settings
    
    # 检查 INSTALLED_APPS
    if 'django_q' in settings.INSTALLED_APPS:
        print("✓ django_q 已添加到 INSTALLED_APPS")
    else:
        print("✗ django_q 未添加到 INSTALLED_APPS")
        return False
    
    # 检查 Q_CLUSTER 配置
    if hasattr(settings, 'Q_CLUSTER'):
        print("✓ Q_CLUSTER 配置存在")
        print(f"  - Workers: {settings.Q_CLUSTER.get('workers', 'N/A')}")
        print(f"  - Timeout: {settings.Q_CLUSTER.get('timeout', 'N/A')}")
    else:
        print("✗ Q_CLUSTER 配置不存在")
        return False
    
    # 检查 LOGGING 配置
    if hasattr(settings, 'LOGGING'):
        print("✓ LOGGING 配置存在")
        if 'ai' in settings.LOGGING.get('loggers', {}):
            print("✓ 'ai' logger 已配置")
        else:
            print("⚠ 'ai' logger 未配置（可选）")
    else:
        print("⚠ LOGGING 配置不存在（可选）")
    
    print()
    return True


def test_management_command():
    """测试管理命令是否可用"""
    print("=" * 60)
    print("测试 4: 管理命令")
    print("=" * 60)
    
    try:
        from django.core.management import get_commands
        commands = get_commands()
        
        if 'init_bots' in commands:
            print("✓ init_bots 管理命令已注册")
            print()
            return True
        else:
            print("✗ init_bots 管理命令未注册")
            print()
            return False
    except Exception as e:
        print(f"✗ 管理命令测试失败: {e}")
        print()
        return False


def main():
    """运行所有测试"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "论坛机器人功能测试" + " " * 20 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    results = []
    
    # 运行测试
    results.append(("模块导入", test_imports()))
    results.append(("数据库模型", test_models()))
    results.append(("Django 配置", test_settings()))
    results.append(("管理命令", test_management_command()))
    
    # 汇总结果
    print("=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name:20s} {status}")
    
    print()
    print(f"总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！论坛机器人功能已成功安装。")
        print("\n下一步:")
        print("1. 设置 OPENAI_API_KEY 环境变量")
        print("2. 使用 init_bots 命令创建机器人账号")
        print("3. 启动 django-q2 worker: python manage.py qcluster")
        print("4. 启动 Django 服务器: python manage.py runserver")
        return 0
    else:
        print("\n⚠ 部分测试失败，请检查上述错误信息。")
        return 1


if __name__ == '__main__':
    sys.exit(main())
