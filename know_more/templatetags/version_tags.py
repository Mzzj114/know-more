# Git needs to work in the system ternimal for this tag to work

from django import template

register = template.Library()


import os

def get_git_version():
    """
    Get version information from environment variables (set during Docker build).
    Returns a dict with commit_hash, commit_date, and version_tag.
    """
    commit_hash = os.environ.get('GIT_COMMIT')
    
    if not commit_hash:
        return None
        
    return {
        'commit_hash': commit_hash,
        'commit_date': os.environ.get('GIT_DATE', ''),
        'version_tag': os.environ.get('GIT_TAG') or None,
    }


@register.simple_tag
def version_info():
    """
    Template tag that returns current git version information.
    Usage: {% version_info %}
    """
    return get_git_version()
