# PromptForGood (智问善答) - 提示词工程学习平台

PromptForGood (智问善答) 是一个面向普及与提升「提示词工程（Prompt Engineering）」技能的非盈利导航与学习平台。用户可以通过交互式教程学习提示词工程知识，在真实场景中练习制定提示词，并在社区论坛中分享和交流经验。

## 项目特点

- **交互式教程**：通过悬浮窗和引导式表单，帮助用户掌握规范提示词结构
- **案例教学**：提供"设计学习路线"等实用案例，引导用户实践提示词技巧
- **LLM 测试环境**：内置大语言模型接入，可实时测试提示词效果
- **社区论坛**：支持发帖、回帖、点赞、收藏，促进提示词模板分享与讨论
- **详细文档**：提供提示词工程理论和技巧的系统性介绍

## 技术栈

### 后端

- Python 3.11+ / Django 4.x
- Django REST Framework
- MySQL 8.0
- uWSGI + Nginx

### 前端

- Vue.js + Element Plus
- Django Templates（传统渲染方式，非前后端分离）

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
git clone <repository-url>
cd know-more
```

2. **配置环境变量**

复制环境变量模板并修改配置：

```bash
cp production.env.template production.env
```

编辑 `production.env` 文件，设置以下关键配置：

- `SECRET_KEY`：Django 密钥（可使用 `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` 生成）

- `DATABASE_URL`：数据库连接字符串（默认已配置）

- `OPENAI_API_KEY` 或 `ANTHROPIC_API_KEY`：LLM API 密钥（用于提示词测试功能）

- 其他可选配置项
3. **启动服务**

```bash
docker-compose up -d
```

首次启动时，Docker 会自动：

- 构建应用镜像

- 初始化 MySQL 数据库

- 安装 Python 和 Node.js 依赖

- 编译国际化消息文件

- 创建必要的目录结构
4. **初始化数据库**

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
docker-compose exec web python manage.py compilemessages
```

5. **创建超级用户**

```bash
docker-compose exec web python manage.py createsuperuser
```

6. **访问应用**

打开浏览器访问：`http://localhost`

- 主站点：`http://localhost/`
- 文档站点：`http://localhost/docs/`
- 论坛站点：`http://localhost/forum/`
- 管理后台：`http://localhost/admin/`

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

## 常用命令

### 容器管理

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f web
docker-compose logs -f nginx
docker-compose logs -f db

# 进入容器
docker-compose exec web bash
docker-compose exec db mysql -u root -p
```

### Django 管理

```bash
# 执行迁移
docker-compose exec web python manage.py migrate

# 收集静态文件
docker-compose exec web python manage.py collectstatic --noinput

# 编译国际化消息
docker-compose exec web python manage.py compilemessages

# 运行测试
docker-compose exec web python manage.py test

# 初始化论坛数据
docker-compose exec web python manage.py init_forum_data
```

### 开发调试

```bash
# 使用开发配置启动（热重载）
docker-compose -f docker-compose.dev.yml up -d

# 查看实时日志
docker-compose logs -f --tail=100 web
```

## 配置说明

### 环境变量

主要配置项位于 `production.env` 文件：

| 变量名              | 说明            | 示例                               |
| ---------------- | ------------- | -------------------------------- |
| `DJANGO_ENV`     | 运行环境          | `prod` / `dev`                   |
| `SECRET_KEY`     | Django 密钥     | （随机字符串）                          |
| `DATABASE_URL`   | 数据库连接         | `mysql://user:pass@host:port/db` |
| `OPENAI_API_KEY` | OpenAI API 密钥 | `sk-...`                         |
| `ALLOWED_HOSTS`  | 允许的主机         | `localhost,example.com`          |
| `DEBUG`          | 调试模式          | `True` / `False`                 |

### Nginx 配置

Nginx 配置文件位于 `nginx/django.conf`，主要功能：

- 反向代理到 uWSGI
- 静态文件服务
- Gzip 压缩
- 安全头设置

## 国际化支持

项目支持中英文双语：

```bash
# 提取翻译字符串
docker-compose exec web python manage.py makemessages -l zh
docker-compose exec web python manage.py makemessages -l en

# 编译翻译文件
docker-compose exec web python manage.py compilemessages
```

翻译文件位于 `locale/` 目录。

## 部署建议

### 生产环境

1. **修改默认密码**
   
   - 更改 MySQL root 密码
   - 设置强 SECRET_KEY

2. **启用 HTTPS**
   
   - 配置 SSL 证书
   - 更新 Nginx 配置

3. **备份策略**
   
   ```bash
   # 备份数据库
   docker-compose exec db mysqldump -u root -p know_more > backup.sql
   
   # 备份静态文件
   tar -czf static-backup.tar.gz staticfiles/
   ```

4. **监控与日志**
   
   - 配置日志轮转
   - 设置健康检查
   - 监控资源使用

### 性能优化

- 启用 Redis 缓存（可选）
- 配置 CDN 加速静态资源
- 优化数据库查询和索引
- 启用 Gzip/Brotli 压缩

## 故障排查

### 常见问题

**1. 容器启动失败**

```bash
# 查看详细日志
docker-compose logs web

# 检查配置文件语法
docker-compose config
```

**2. 数据库连接错误**

```bash
# 检查数据库健康状态
docker-compose ps db

# 查看数据库日志
docker-compose logs db
```

**3. 静态文件 404**

```bash
# 重新收集静态文件
docker-compose exec web python manage.py collectstatic --noinput --clear

# 检查权限
docker-compose exec web ls -la /app/staticfiles
```

**4. 国际化不生效**

```bash
# 重新编译消息文件
docker-compose exec web python manage.py compilemessages

# 检查 locale 目录权限
docker-compose exec web ls -la /app/locale
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

---

**注意**：本项目为非盈利公益项目，旨在降低 AI 使用门槛，让更多人能够高效、可控地使用大语言模型。
