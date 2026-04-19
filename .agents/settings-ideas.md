# 二、推荐方案（行业主流）

## ✅ 结构：拆成 settings 包

```bash
project/
  settings/
    __init__.py
    base.py
    dev.py
    prod.py
```

这是 Django 社区最常见的做法 ([Medium][2])

---

## ✅ 思路：三层结构

### 1️⃣ base.py（通用配置）

```python
# settings/base.py

INSTALLED_APPS = [...]
MIDDLEWARE = [...]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"

STATIC_URL = "/static/"
```

👉 只放“永远不会因环境改变”的东西

---

### 2️⃣ dev.py（开发环境）

```python
from .base import *

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

---

### 3️⃣ prod.py（生产环境）

```python
from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = ["yourdomain.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": os.environ["DB_HOST"],
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
    }
}

SECURE_SSL_REDIRECT = True
```

---

## ✅ 启动方式（关键）

### 本地开发：

```bash
python manage.py runserver --settings=project.settings.dev
```

---

### 生产（Docker / gunicorn / uwsgi）：

```bash
export DJANGO_SETTINGS_MODULE=project.settings.prod
```

---

# 三、环境变量

你现在用：

* AWS RDS
* Cloudflare
* Docker

👉 强烈建议：

### 所有敏感信息必须进环境变量

比如：

```env
SECRET_KEY=xxx
DB_PASSWORD=xxx
```

然后：

```python
import os
SECRET_KEY = os.environ["SECRET_KEY"]
```

---

💡 这点非常重要：

* 不要把 secret 写在 settings 文件里
* 不要 commit 到 Git

---


### 可选：自动切换

```python
# settings/__init__.py
import os

env = os.getenv("DJANGO_ENV", "dev")

if env == "prod":
    from .prod import *
else:
    from .dev import *
```

然后：

```bash
export DJANGO_ENV=prod
```

---

[1]: https://docs.djangoproject.com/en/4.2/ref/settings/?utm_source=chatgpt.com "Settings | Django documentation | Django"
[2]: https://medium.com/django-unleashed/django-settings-best-practices-for-organizing-your-configuration-529ac38606cc?utm_source=chatgpt.com "Django Settings: Best Practices for Organizing Your Configuration | by Samuel Getachew | Django Unleashed | Medium"
