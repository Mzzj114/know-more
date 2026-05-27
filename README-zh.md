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

PromptForGood (智问善答) 是一个面向普及与提升提示词工程（Prompt Engineering）技能的非盈利学习平台。用户可以通过交互式教程学习提示词工程知识，在真实场景中练习制定提示词，并在社区论坛中分享和交流经验。

## 项目特点

- **交互式教程**：通过悬浮窗和引导式表单，帮助用户掌握规范提示词结构
- **LLM 测试环境**：内置大语言模型接入，可实时测试提示词效果
- **社区论坛**：支持发帖、回帖、点赞、收藏，促进提示词模板分享与讨论
- **详细文档**：提供提示词工程理论和技巧的系统性介绍

## 技术栈

### 后端

- Python 3.11 / Django 5.x
- Django REST Framework
- MySQL 8.0
- uWSGI + Nginx

### 前端

- Vue.js + Element Plus (使用 Node.js + npm 构建前端)
- Django Templates（传统渲染方式，非 SPA）

### 基础设施

- Docker + Docker Compose
- GitHub Actions（CI/CD）

## 快速开始

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+

### 安装步骤

1. **克隆仓库**

```bash
git clone https://github.com/Mzzj114/know-more.git
cd know-more
```

2. **配置环境变量**

复制环境变量模板并修改配置：

```bash
cp production.env.template production.env
```

编辑 `production.env` 文件，具体配置参考 `know-more/settings/prod.py`，并根据实际情况修改。

更多信息参考 [Django官方文档](https://docs.djangoproject.com/)

3. **启动服务**

使用启动脚本：

```bash
./scripts/prod/launch.sh
```

项目本质上是 docker 项目，详情参考 [官方文档](https://docs.docker.com/)

## 项目结构

```
know-more/
├── account/          # 用户认证模块
├── ai/               # AI/LLM 接入层
├── docs/             # 文档站点（Flat-file CMS）
├── document/         # Markdown 文档源文件
├── forum/            # 论坛模块
├── main/             # 主站点（首页、教程、案例）
├── know_more/        # Django 项目配置
├── static/           # 静态资源（CSS、JS、教程数据）
├── templates/        # Django 模板
├── locale/           # 国际化翻译文件
├── nginx/            # Nginx 配置文件
├── scripts/          # 启动脚本
├── Dockerfile        # Docker 镜像构建文件
├── docker-compose.yml # Docker Compose 配置
└── requirements.txt  # Python 依赖
```

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
- 问题反馈：[Issues](https://github.com/Mzzj114/know-more/issues)
- 邮箱：mzzj139@gmail.com

## 致谢

感谢所有为提示词工程普及做出贡献的开发者和社区成员。
