👉 **推荐你用：统一的 URL 语言前缀（i18n_patterns）+ LocaleMiddleware**

也就是：

```text
/en/xxx
/zh/xxx
```

并且：

* 所有内容（CMS + Django templates）统一走这个机制
* 不要分开处理（❌ 不要 CMS 一套、template 一套）

# “base.html 下拉框”怎么处理？

用 Django 提供的方式生成“语言切换 URL”：

```django
{% load i18n %}

{% get_available_languages as languages %}
{% for lang_code, lang_name in languages %}
    {% language lang_code %}
        <a href="{% url 'current_view_name' %}">
            {{ lang_name }}
        </a>
    {% endlanguage %}
{% endfor %}
```

👉 自动跳到：

```text
/en/xxx
/zh/xxx
```

---

# 四、一个你现在最适合的架构（很具体）

## 1️⃣ settings.py

```python
LANGUAGES = [
    ('en', 'English'),
    ('zh', 'Chinese'),
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]
```

---

## 2️⃣ urls.py（关键）

```python
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    prefix_default_language=True,
)
```

## 3️⃣ CMS 加载

```python
lang = request.LANGUAGE_CODE
content = load(f"content/{lang}/page.md")
```

但是考虑到项目只打算支持中文和英文，要把所有可能的 LANGUAGE_CODE 都归一化为 zh 或 en （按照国际惯例，默认 en）

建议把现在的 zh-Hans 和 en-US 目录名改为更简洁的 zh 和 en