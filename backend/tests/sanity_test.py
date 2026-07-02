from django.conf import settings


def test_django_boots_with_development_settings() -> None:
    assert settings.SETTINGS_MODULE == 'config.settings.development'
    assert settings.CACHES['default']['BACKEND'].endswith('RedisCache')
