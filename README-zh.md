# PromptForGood (智问善答)

<p align="center">
  <a href="https://github.com/Mzzj114/know-more">
    <img src="static/img/logo.png" alt="PromptForGood Logo" width="120" height="120">
  </a>
</p>

<p align="center">
  <b>简体中文</b> | <a href="README.md">English</a>
</p>

<p align="center">
  <a href="https://github.com/Mzzj114/know-more/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-GPLv3-blue.svg" alt="License">
  </a>
  <img src="https://img.shields.io/badge/python-3.11-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/django-5.x-green.svg" alt="Django Version">
  <img src="https://img.shields.io/badge/vuejs-3.x-4fc08d.svg" alt="Vue.js Version">
  <img src="https://img.shields.io/badge/element--plus-2.x-409eff.svg" alt="Element Plus Version">
</p>

**PromptForGood**（智问善答）是一个面向普及与提升提示词工程（Prompt Engineering）技能的非盈利学习平台。用户可以通过交互式教程学习提示词工程知识，在真实场景中练习制定提示词，并在社区论坛中分享和交流经验。

平台已上线：**[know-more.mzzj.org](https://know-more.mzzj.org)**

## 项目特点

- **交互式教程**：逐步引导的互动教程，涵盖从基础概念到高级技巧（如思维链、元提示、对抗提示等）的丰富内容。以悬浮窗和引导式表单呈现，帮助用户掌握规范提示词结构。
- **LLM 对话环境**：内置大语言模型聊天界面（基于 OpenAI API），可实时测试提示词效果。匿名用户每周 5,000 tokens，注册用户每周 50,000 tokens。
- **社区论坛**：功能完善的论坛系统，支持发帖、回复（楼中楼）、点赞、收藏和分类浏览，促进提示词模板与技巧的分享与讨论。
- **文档站点**：基于文件的 CMS 系统，从 `document/` 目录读取 Markdown 文档，支持 Frontmatter 元数据、侧边栏导航和中英文多语言。
- **论坛 AI 机器人**：自动 Bot 账号模拟用户在论坛中的互动。通过 `BotProfile` 配置，由 Django Q2 调度周期性操作。
- **多语言**：完整支持中英文国际化，通过 LocaleMiddleware 自动切换语言。

## 技术栈

### 后端

- **Python 3.11** / **Django 5.x**
- Django REST Framework（论坛 API 端点）
- MySQL 8.0（生产）/ SQLite3（开发）
- uWSGI + Nginx（生产部署）
- Django Q2（异步任务队列，用于论坛机器人）
- django-anymail（通过 Resend 发送邮件）
- python-frontmatter & markdown（文档渲染）

### 前端

- **Vue 3** + **Element Plus**（嵌入在 Django 模板中的互动组件）
- axios、marked、Vditor（Markdown 编辑器）、reveal.js（幻灯片）
- Node.js 20 + npm（前端构建）

### 基础设施

- Docker + Docker Compose（MySQL、Web、Nginx、qcluster 四个服务）
- GitHub Actions（CI/CD 流水线）
- Cloudflare（DNS、SSL、Turnstile 机器人防护）
- AWS EC2 + RDS（生产服务器托管）

## 项目结构

```
know-more/
├── account/            # 用户认证模块
│   ├── views.py        # 登录、注册、密码重置（邮箱验证码）
│   ├── forms.py        # 自定义用户注册表单
│   └── urls.py         # 认证 URL 路由
├── ai/                 # AI/LLM 接入层
│   ├── views.py        # OpenAI 聊天 API + Token 管理
│   ├── models.py       # UserTokenUsage, BotProfile, BotActionLog
│   └── urls.py         # /ai/chat/ 端点
├── docs/               # 文档站点（Flat-file CMS）
│   ├── views.py        # 文档索引和详情视图
│   ├── utils.py        # Markdown 读取、Frontmatter 解析、路径穿越防护
│   └── urls.py         # /docs/ URL 路由
├── document/           # Markdown 文档源文件
│   ├── en/             # 英文文档
│   └── zh/             # 中文文档
├── forum/              # 论坛模块
│   ├── models.py       # Category, Post, Reply, Like, Favorite, UserProfile
│   ├── views.py        # 模板视图 + DRF API 视图
│   ├── serializers.py  # DRF 序列化器
│   ├── services.py     # 业务逻辑层
│   ├── signals.py      # 统计更新信号处理器
│   └── management/     # 自定义命令（init_forum_data）
├── main/               # 主站点（首页、教程、幻灯片）
│   ├── views.py        # 首页、教程（Vue 驱动）、幻灯片
│   ├── urls.py         # 主站 URL 路由 + 教程 API
│   └── admin_views.py  # 管理后台发送邮件视图
├── know_more/          # Django 项目配置
│   ├── settings/       # 设置包
│   │   ├── base.py     # 通用配置
│   │   ├── dev.py      # 开发环境（SQLite、console 邮件）
│   │   └── prod.py     # 生产环境（MySQL、Resend 邮件、安全配置）
│   ├── urls.py         # 根 URL 配置（含 i18n_patterns）
│   ├── wsgi.py         # WSGI 入口
│   ├── asgi.py         # ASGI 入口
│   └── templatetags/   # 自定义模板标签（version_tags）
├── static/             # 静态资源
│   ├── tutorials/      # 教程 JSON 数据（en/zh）
│   └── img/            # 图片
├── templates/          # Django 模板
│   ├── admin/          # 管理后台自定义模板
│   ├── auth/           # 登录、注册、密码重置
│   ├── docs/           # 文档页面
│   ├── forum/          # 论坛页面
│   └── main/           # 首页、教程、幻灯片
├── locale/             # 国际化翻译文件
│   ├── en/             # 英文翻译
│   └── zh/             # 中文翻译
├── nginx/              # Nginx 配置文件
├── scripts/            # 部署脚本
│   ├── prod/           # 生产启动脚本
│   └── entrypoint.sh   # Docker 入口（迁移、静态文件收集、uWSGI）
├── env/                # 环境变量文件（已加入 gitignore）
├── .agents/            # AI agent 规则和技能
│   ├── rules/          # Agent 行为规则
│   └── skills/         # Agent 技能
├── Dockerfile          # 多阶段 Docker 构建（Node 构建 + Python）
├── docker-compose.yml  # Docker Compose 配置（4 个服务）
├── requirements.txt    # Python 依赖
├── package.json        # Node.js 依赖（Vue 3、Element Plus 等）
├── manage.py           # Django 管理脚本
├── uwsgi.ini           # uWSGI 配置
└── sitemap.py          # Sitemap 配置
```

## 快速开始

### 前置要求

- Python 3.11+
- Node.js 20+ & npm
- Docker 20.10+ & Docker Compose 2.0+（生产部署用）

### 开发环境

1. **克隆仓库**

   ```bash
   git clone https://github.com/Mzzj114/know-more.git
   cd know-more
   ```

2. **设置 Python 虚拟环境**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **安装前端依赖**

   ```bash
   npm install
   ```

4. **配置环境变量**

   ```bash
   cp env/production.env.template env/development.env
   # 编辑 env/development.env
   ```

   你也可以直接创建 `env/development.env` 文件，参考 `know_more/settings/dev.py` 了解需要的环境变量。

5. **运行数据库迁移**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **编译翻译文件**

   ```bash
   python manage.py compilemessages
   ```

7. **启动开发服务器**

   ```bash
   python manage.py runserver --settings=know_more.settings.dev
   ```

   访问 `http://127.0.0.1:8000/`

### 生产部署 (Docker)

1. **配置生产环境变量**

   ```bash
   cp env/production.env.template env/production.env
   ```

2. **启动服务**

   ```bash
   # 首次部署或代码变更后：
   ./scripts/prod/launch.sh --build

   # 正常重启：
   ./scripts/prod/launch.sh
   ```

   这将启动 4 个 Docker 服务：
   - `db` — MySQL 8.0 数据库
   - `web` — Django 应用（uWSGI）
   - `nginx` — Nginx 反向代理
   - `qcluster` — Django Q2 任务调度器

## 贡献指南

欢迎贡献代码、文档或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 [GNU v3 License](LICENSE) 开源协议。

## 联系方式

- 项目主页：[GitHub Repository](https://github.com/Mzzj114/know-more)
- 线上站点：[know-more.mzzj.org](https://know-more.mzzj.org)
- 问题反馈：[Issues](https://github.com/Mzzj114/know-more/issues)
- 邮箱：mzzj139@gmail.com

## 致谢

感谢所有为提示词工程普及做出贡献的开发者和社区成员。
