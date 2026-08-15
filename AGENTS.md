# AGENTS.md — PromptForGood (know-more)

## Project Overview

**PromptForGood** (智问善答) is a non-profit open-source learning platform dedicated to popularizing prompt engineering skills. Users learn through interactive tutorials, test prompts via a built-in LLM chat interface (OpenAI), and engage in a community forum to share prompt templates and techniques.

- **Repository**: https://github.com/Mzzj114/know-more
- **Live Site**: https://promptforgood.org
- **License**: GPLv3

## Technology Stack

| Layer | Technologies |
|-------|-------------|
| Backend | Python 3.11, Django 5.x, Django REST Framework |
| Database | MySQL 8.0 (prod), SQLite3 (dev) |
| Frontend | Vue 3, Element Plus, Vditor, marked, reveal.js |
| Server | uWSGI, Nginx, Docker Compose |
| Task Queue | Django Q2 (qcluster) |
| Email | django-anymail + Resend |
| Bot Protection | Cloudflare Turnstile |
| CI/CD | GitHub Actions |
| Hosting | AWS EC2 + RDS |

## Project Structure

```
know-more/
├── account/             # User auth (login, register, password reset, Cloudflare Turnstile)
├── ai/                  # AI/LLM chat API, token management, forum bot profiles
├── docs/                # Flat-file documentation CMS (reads Markdown from document/)
├── document/            # Documentation source files (en/zh)
├── forum/               # Forum (Category, Post, Reply, Like, Favorite)
├── main/                # Home page, interactive tutorials (Vue-driven), slides
├── know_more/           # Django project config
│   └── settings/        # Settings package (base.py, dev.py, prod.py)
├── static/              # Static assets (CSS, JS, tutorial JSON data, images)
├── templates/           # Django templates (admin, auth, docs, forum, main)
├── locale/              # i18n translation files (en, zh)
├── nginx/               # Nginx configuration
├── scripts/             # Deployment and entrypoint scripts
├── env/                 # Environment variable files (gitignored)
├── .agents/             # AI agent rules and skills
├── Dockerfile           # Multi-stage Docker build
├── docker-compose.yml   # 4 services: db, web, nginx, qcluster
├── uwsgi.ini            # uWSGI configuration
├── sitemap.py           # Sitemap configuration
├── requirements.txt     # Python dependencies
└── package.json         # Node.js dependencies
```

## Key Django Apps

### `account`
- Custom login, registration, and password reset
- Email verification codes (cached, 5-minute expiry)
- Cloudflare Turnstile bot protection on all auth forms
- Language-aware with Django i18n

### `ai`
- **Chat API** (`/ai/chat/`): OpenAI integration with weekly token quota (5K anonymous, 50K registered)
- **Bot System**: `BotProfile`, `BotActionLog` models for forum automation bots
- Django Q2 scheduler for periodic bot actions (posting, replying, liking)

### `docs`
- **Flat-file CMS**: Reads Markdown from `document/{lang}/`, renders with python-markdown
- Frontmatter metadata: title, slug, order, tags
- Directory traversal protection in `utils.py`
- i18n-aware: content switches with language

### `forum`
- **Models**: Category, Post, Reply, Like, Favorite, UserProfile
- **Template views**: Forum index, category detail, post detail, user profile
- **DRF APIs**: CRUD endpoints for posts, replies, likes, favorites
- **Features**: Pagination, nested replies, Markdown content, auto-floor numbering
- **Signals**: Auto-update counts on likes/favorites

### `main`
- **Home page**: Static template with navigation
- **Tutorials**: Vue-driven interactive tutorials loaded from `static/tutorials/{lang}/*.json`
- **Slides**: reveal.js presentation viewer

## Development Setup

```bash
# Python venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
npm install

# Database
python manage.py makemigrations
python manage.py migrate

# i18n
python manage.py compilemessages

# Run
python manage.py runserver --settings=know_more.settings.dev
```

## Production Deployment

```bash
# Docker Compose
./scripts/prod/launch.sh --build
```

Services: `db` (MySQL 8.0), `web` (uWSGI Django), `nginx`, `qcluster` (Django Q2).

## Environment Variables

Key env vars (configured in `env/` directory):

| Variable | Purpose |
|----------|---------|
| SECRET_KEY | Django secret key |
| DATABASE_URL | Database connection string |
| OPENAI_API_KEY | OpenAI API key for chat |
| RESEND_API_KEY | Resend API key for email |
| CLOUDFLARE_TURNSTILE_* | Turnstile site/secret keys |
| DJANGO_ENV | `dev` or `prod` |
| AI_API_KEY / AI_API_URL | Alternative AI provider |

## Important Notes for AI Agents

1. **Never push to remote** — only local commits unless explicitly directed.
2. **`.agents/` directory** contains project rules and skills that guide agent behavior.
3. **Settings split** into `base.py` / `dev.py` / `prod.py` — use `--settings=know_more.settings.dev` for development.
4. **i18n**: All URLs use `i18n_patterns` with language prefix (`/en/`, `/zh/`).
5. **Static files**: Served from `static/` directory; frontend dependencies are vendored into `static/vendor/` from `node_modules/` at build time, so `node_modules/` itself is no longer exposed via `/static/`. Change Dockerfile when new frontend dependencies are included.
6. **Documentation source**: Lives in `document/{lang}/` as Markdown with frontmatter — this is the Flat-file CMS content.
7. **Tutorial data**: Lives in `static/tutorials/{lang}/*.json` — this is separate from the documentation.
8. **Requirements.txt** is the exact pip freeze output — use it for venv setup.
