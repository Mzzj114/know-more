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

PromptForGood (智问善答) is a non-profit learning platform dedicated to popularizing and improving prompt engineering skills. Users can learn prompt engineering concepts through interactive tutorials, practice crafting prompts in real-world scenarios, and share and exchange experiences in the community forum.

## Key Features

- **Interactive Tutorials**: Help users master standard prompt structures through floating windows and guided forms.
- **LLM Test Environment**: Integrated Large Language Model (LLM) access for real-time testing of prompt effects.
- **Community Forum**: Supports posting, replying, liking, and bookmarking to promote sharing and discussion of prompt templates.
- **Detailed Documentation**: Provides a systematic introduction to prompt engineering theory and techniques.

## Technology Stack

### Backend

- Python 3.11 / Django 5.x
- Django REST Framework
- MySQL 8.0
- uWSGI + Nginx

### Frontend

- Vue.js + Element Plus (Node.js + npm used for frontend)
- Django Templates (Traditional rendering, not SPA)

### Infrastructure

- Docker + Docker Compose
- GitHub Actions (CI/CD)

## Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

### Installation Steps

1. **Clone the Repository**

```bash
git clone https://github.com/Mzzj114/know-more.git
cd know-more
```

2. **Configure Environment Variables**

Copy the environment variable template and modify the configuration:

```bash
cp production.env.template production.env
```

Edit the `production.env` file. Refer to `know-more/settings/prod.py` for specific configurations and modify them based on your actual setup.

For more information, refer to the [Django Official Documentation](https://docs.djangoproject.com/).

3. **Start the Services**

Use the startup script:

```bash
./scripts/prod/launch.sh
```

The project is essentially a Docker project. For details, refer to the [Official Docker Documentation](https://docs.docker.com/).

## Project Structure

```
know-more/
├── account/          # User authentication module
├── ai/               # AI/LLM integration layer
├── docs/             # Documentation site (Flat-file CMS)
├── document/         # Markdown documentation source files
├── forum/            # Forum module
├── main/             # Main site (Home page, tutorials, use cases)
├── know_more/        # Django project settings & configuration
├── static/           # Static assets (CSS, JS, tutorial data)
├── templates/        # Django templates
├── locale/           # Internationalization (i18n) translation files
├── nginx/            # Nginx configurations
├── scripts/          # Startup and deployment scripts
├── Dockerfile        # Dockerfile for image builds
├── docker-compose.yml # Docker Compose configuration
└── requirements.txt  # Python dependencies
```

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
- Feedback & Issues: [Issues](https://github.com/Mzzj114/know-more/issues)
- Email: mzzj139@gmail.com

## Acknowledgements

Thanks to all the developers and community members who have contributed to popularizing prompt engineering.
