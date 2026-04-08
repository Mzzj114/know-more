# Git needs to work in the system ternimal for this tag to work

import subprocess
from django import template

register = template.Library()


def get_git_version():
    """
    Get version information from git repository.
    Returns a dict with commit_hash, commit_date, and version_tag.
    """
    try:
        # Get short commit hash
        commit_hash = subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD'],
            stderr=subprocess.DEVNULL,
            encoding='utf-8'
        ).strip()
        print(f'Commit hash: {commit_hash}')
        
        # Get commit date
        commit_date = subprocess.check_output(
            ['git', 'log', '-1', '--date=short', '--format=%cd'],
            stderr=subprocess.DEVNULL,
            encoding='utf-8'
        ).strip()
        print(f'Commit date: {commit_date}')
        
        # Try to get version tag (may fail if no tags exist)
        try:
            version_tag = subprocess.check_output(
                ['git', 'describe', '--tags', '--always'],
                stderr=subprocess.DEVNULL,
                encoding='utf-8'
            ).strip()
            print(f'Version tag: {version_tag}')
        except subprocess.CalledProcessError:
            version_tag = None
            
        return {
            'commit_hash': commit_hash,
            'commit_date': commit_date,
            'version_tag': version_tag,
        }
    except Exception:
        # Return None if git is not available or not in a git repo
        return None


@register.simple_tag
def version_info():
    """
    Template tag that returns current git version information.
    Usage: {% version_info %}
    """
    return get_git_version()
