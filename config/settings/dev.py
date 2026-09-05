from .base import *

# Development settings override
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

# In development, enable console email backend if needed
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
