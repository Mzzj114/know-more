import os

# Automatic environment switching based on DJANGO_ENV environment variable
# Default to 'dev' if not set
env_name = os.getenv('DJANGO_ENV', 'dev').lower()

if env_name == 'prod':
    from .prod import *
elif env_name == 'dev':
    from .dev import *
else:
    # Fallback or custom environments
    try:
        if env_name == 'base':
            from .base import *
        else:
            # Try to import from a file named after the environment
            import importlib
            module = importlib.import_module(f'.{env_name}', __package__)
            from_module = {k: v for k, v in module.__dict__.items() if not k.startswith('_')}
            globals().update(from_module)
    except ImportError:
        # Final fallback to dev
        from .dev import *
