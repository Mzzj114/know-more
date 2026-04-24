# Sitemap 设置说明

## 概述

本项目已集成 Django Sitemap 功能，用于生成网站的 sitemap.xml 文件，帮助搜索引擎更好地索引网站内容。

## 配置步骤

### 1. 数据库迁移

在首次部署或创建新数据库时，需要运行以下命令：

```bash
python manage.py migrate
```

这将应用包括 `sites` 框架在内的所有迁移。

### 2. 设置默认站点

Django 的 Sitemap 功能依赖于 Sites 框架。每次创建新数据库后，需要设置默认站点。

#### Linux/Mac:
```bash
chmod +x scripts/setup_site.sh
./scripts/setup_site.sh [domain] [site_name]
```

示例：
```bash
./scripts/setup_site.sh example.com "PromptForGood"
```

#### Windows:
```cmd
scripts\setup_site.bat [domain] [site_name]
```

示例：
```cmd
scripts\setup_site.bat example.com "PromptForGood"
```

如果不提供参数，将使用默认值：
- Domain: `localhost:8000`
- Site Name: `PromptForGood`

### 3. 访问 Sitemap

设置完成后，可以通过以下 URL 访问 sitemap：

```
http://your-domain/sitemap.xml
```

## Sitemap 包含的内容

当前 sitemap 包含以下内容：

1. **静态页面**: 首页、文档索引页、论坛首页
2. **文档页面**: 所有 Markdown 文档
3. **论坛帖子**: 所有活跃的论坛帖子
4. **论坛分类**: 所有论坛分类

## 生产环境部署

在生产环境中部署时，请确保：

1. 运行数据库迁移
2. 执行 `setup_site.sh` 或 `setup_site.bat` 脚本，使用正确的域名
3. 确保 Nginx 配置正确（已包含在 `nginx/django.conf` 中）

## 注意事项

- 每次创建新数据库时都需要运行 setup_site 脚本
- 如果更改了域名，需要重新运行 setup_site 脚本更新配置
- Sitemap 会自动更新，无需手动维护
