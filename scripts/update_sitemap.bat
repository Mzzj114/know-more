@echo off
REM 设置 Django Sites framework 的默认站点
REM 使用方法: setup_site.bat [domain] [site_name]
REM 示例: setup_site.bat example.com "My Site"

setlocal

if "%1"=="" (
    set DOMAIN=localhost:8000
) else (
    set DOMAIN=%1
)

if "%2"=="" (
    set SITE_NAME=Know More
) else (
    set SITE_NAME=%2
)

echo Setting up default site...
echo Domain: %DOMAIN%
echo Site Name: %SITE_NAME%

python manage.py shell -c "from django.contrib.sites.models import Site; site, created = Site.objects.update_or_create(id=1, defaults={'domain': '%DOMAIN%', 'name': '%SITE_NAME%'}); print(f'Created new site: {site.domain} - {site.name}' if created else f'Updated existing site: {site.domain} - {site.name}'); print('Site setup completed successfully!')"

echo Done!
