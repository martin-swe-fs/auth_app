from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse


def check_db() -> bool:
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            return bool(cursor.fetchone() == (1,))
    except Exception:
        return False


def check_redis() -> bool:
    try:
        cache.set('healthz', 'ok', timeout=60)
        return bool(cache.get('healthz') == 'ok')
    except Exception:
        return False


def healthz(request) -> JsonResponse:
    db_ok = check_db()
    redis_ok = check_redis()
    response_status_code = 200 if db_ok and redis_ok else 503

    return JsonResponse(
        {
            'db': 'ok' if db_ok else 'error',
            'redis': 'ok' if redis_ok else 'error',
        },
        status=response_status_code,
    )
