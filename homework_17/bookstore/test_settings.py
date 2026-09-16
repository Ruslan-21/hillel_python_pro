from .settings import *

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.getenv(
            "CACHE_URL",
            "redis://redis:6379/2",
        ),
    }
}
