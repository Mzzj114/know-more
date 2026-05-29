#!/bin/bash
# 设置 Django Sites framework 的默认站点
# 使用方法: ./scripts/setup_site.sh [domain] [site_name]
# 示例: ./scripts/setup_site.sh example.com "My Site"

set -e

DOMAIN=${1:-"localhost:8000"}
SITE_NAME=${2:-"Know More"}

echo "Setting up default site..."
echo "Domain: $DOMAIN"
echo "Site Name: $SITE_NAME"

python manage.py shell << EOF
from django.contrib.sites.models import Site

# 更新或创建默认站点 (id=1)
site, created = Site.objects.update_or_create(
    id=1,
    defaults={
        'domain': '$DOMAIN',
        'name': '$SITE_NAME'
    }
)

if created:
    print(f"Created new site: {site.domain} - {site.name}")
else:
    print(f"Updated existing site: {site.domain} - {site.name}")

print("Site setup completed successfully!")
EOF

echo "Done!"
