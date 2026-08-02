# PromptForGood (智问善答)

<p align="center">
  <a href="https://github.com/Mzzj114/know-more">
    <img src="static/img/logo.png" alt="PromptForGood Logo" width="120" height="120">
  </a>
</p>

<p align="center">
  <a href="README-zh.md">简体中文</a> | <b>English</b>
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

**PromptForGood** (Chinese name: 智问善答) is a non-profit learning platform dedicated to popularizing and improving prompt engineering skills. Users can learn prompt engineering concepts through interactive tutorials, practice crafting prompts in real-world scenarios, and share and exchange experiences in the community forum.

The platform is live at **[promptforgood.org](https://promptforgood.org)**.

## Key Features

- **Interactive Tutorials**: Step-by-step tutorials presented as floating windows and guided forms, covering topics from basic concepts to advanced techniques like Chain-of-Thought, meta-prompting, and adversarial prompting.
- **LLM Chat Environment**: Built-in LLM chat interface (powered by OpenAI) for real-time testing of prompt effects. Token usage is reset weekly — 5,000 tokens for anonymous users and 50,000 tokens for registered users.
- **Community Forum**: Full-featured forum supporting posting, replying (with nested threads), liking, bookmarking, and category browsing. Promotes the sharing and discussion of prompt templates and techniques.
- **Documentation Site**: Flat-file CMS reading Markdown documents from the `document/` directory with frontmatter metadata, sidebar navigation, and multi-language support (English & Chinese).
- **Forum AI Bots**: Automated bot accounts that simulate user interactions in the forum. Configured via `BotProfile` and scheduled with Django Q2 for periodic actions.
- **Multi-language**: Full i18n support for English and Chinese, with locale middleware and language switcher.

## Technology Stack

### Backend

- **Python 3.11** / **Django 5.x**
- Django REST Framework (forum API endpoints)
- MySQL 8.0 (production) / SQLite3 (development)
- uWSGI + Nginx (production deployment)
- Django Q2 (async task queue for forum bots)
- django-anymail (email delivery via Resend)
- python-frontmatter & markdown (documentation rendering)

### Frontend

- **Vue 3** + **Element Plus** (interactive components embedded in Django templates)
- axios, marked, Vditor (Markdown editor), reveal.js (slides)
- Node.js 20 + npm (frontend build)

### Infrastructure

- Docker + Docker Compose (MySQL, web, Nginx, qcluster services)
- GitHub Actions (CI/CD pipeline)
- Cloudflare (DNS, SSL, Turnstile bot protection)
- AWS EC2 + RDS (production hosting)

## Project Structure

```
know-more/
├── account/            # User authentication module
│   ├── views.py        # Login, register, password reset with email verification
│   ├── forms.py        # Custom user creation form
│   └── urls.py         # Auth URL routing
├── ai/                 # AI/LLM integration layer
│   ├── views.py        # OpenAI chat API with token management
│   ├── models.py       # UserTokenUsage, BotProfile, BotActionLog
│   └── urls.py         # /ai/chat/ endpoint
├── docs/               # Documentation site (Flat-file CMS)
│   ├── views.py        # Doc index and detail views
│   ├── utils.py        # Markdown reading, frontmatter parsing, directory traversal protection
│   └── urls.py         # /docs/ URLs
├── document/           # Markdown documentation source files
│   ├── en/             # English docs
│   └── zh/             # Chinese docs
├── forum/              # Forum module
│   ├── models.py       # Category, Post, Reply, Like, Favorite, UserProfile
│   ├── views.py        # Template views + DRF API views
│   ├── serializers.py  # DRF serializers
│   ├── services.py     # Business logic layer
│   ├── signals.py      # Signal handlers for stats updates
│   └── management/     # Custom management commands (init_forum_data)
├── main/               # Main site (home page, tutorials, slides)
│   ├── views.py        # Home, tutorials (Vue-driven), slides
│   ├── urls.py         # Main URL routing + tutorial API
│   └── admin_views.py  # Admin send-email view
├── know_more/          # Django project settings & configuration
│   ├── settings/       # Settings package
│   │   ├── base.py     # Common configuration
│   │   ├── dev.py      # Development settings (SQLite, console email)
│   │   └── prod.py     # Production settings (MySQL, Resend email, security)
│   ├── urls.py         # Root URL config with i18n_patterns
│   ├── wsgi.py         # WSGI entry point
│   ├── asgi.py         # ASGI entry point
│   └── templatetags/   # Custom template tags (version_tags)
├── static/             # Static assets
│   ├── tutorials/      # Tutorial JSON data (en/zh)
│   └── img/            # Images
├── templates/          # Django templates
│   ├── admin/          # Admin custom templates
│   ├── auth/           # Login, register, password reset
│   ├── docs/           # Documentation pages
│   ├── forum/          # Forum pages (index, category, post detail, user profile)
│   └── main/           # Home, tutorial, slides
├── locale/             # Internationalization (i18n) translation files
│   ├── en/             # English translations
│   └── zh/             # Chinese translations
├── nginx/              # Nginx configuration files
├── scripts/            # Deployment scripts
│   ├── prod/           # Production launch scripts
│   └── entrypoint.sh   # Docker entrypoint (migrations, collectstatic, uWSGI)
├── env/                # Environment variable files (gitignored)
├── .agents/            # AI agent rules and skills
│   ├── rules/          # Agent behavior rules
│   └── skills/         # Agent skills (frontend-design, domain-name-brainstormer)
├── Dockerfile          # Multi-stage Docker build (Node builder + Python)
├── docker-compose.yml  # Docker Compose configuration (4 services)
├── requirements.txt    # Python dependencies
├── package.json        # Node.js dependencies (Vue 3, Element Plus, etc.)
├── manage.py           # Django management script
├── uwsgi.ini           # uWSGI configuration
└── sitemap.py          # Sitemap configuration
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+ & npm
- Docker 20.10+ & Docker Compose 2.0+ (for production deployment)

### Development Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Mzzj114/know-more.git
   cd know-more
   ```

2. **Set Up Python Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install Frontend Dependencies**

   ```bash
   npm install
   ```

4. **Configure Environment Variables**

   ```bash
   cp env/production.env.template env/development.env
   # Edit env/development.env with your settings
   ```

   You can also create a `env/development.env` file with environment variables. Refer to `know_more/settings/dev.py` for the expected variables.

5. **Run Database Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Compile Translation Messages**

   ```bash
   python manage.py compilemessages
   ```

7. **Start Development Server**

   ```bash
   python manage.py runserver --settings=know_more.settings.dev
   ```

   The site will be available at `http://127.0.0.1:8000/`.

### Production Deployment (Docker)

1. **Configure Production Environment Variables**

   ```bash
   cp env/production.env.template env/production.env
   # Edit production.env with your production settings
   ```

2. **Launch the Services**

   ```bash
   # First time or after code changes:
   ./scripts/prod/launch.sh --build

   # Normal restart:
   ./scripts/prod/launch.sh
   ```

   This starts 4 Docker services:
   - `db` — MySQL 8.0
   - `web` — Django app (uWSGI)
   - `nginx` — Nginx reverse proxy
   - `qcluster` — Django Q2 task scheduler

## Contribution Guide

Contributions to code, documentation, or suggestions are welcome!

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the [GNU v3 License](LICENSE).

## Contact

- Project Homepage: [GitHub Repository](https://github.com/Mzzj114/know-more)
- Live Site: [promptforgood.org](https://promptforgood.org)
- Feedback & Issues: [Issues](https://github.com/Mzzj114/know-more/issues)
- Email: mzzj139@gmail.com

## Acknowledgements

Thanks to all the developers and community members who have contributed to popularizing prompt engineering.
