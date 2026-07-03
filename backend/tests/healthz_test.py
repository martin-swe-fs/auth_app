import pytest
from django.core.cache import cache
from django.db import connection
from django.test import Client


@pytest.mark.django_db
def test_healthz_returns_ok_when_dependencies_are_up(client: Client) -> None:
    response = client.get('/healthz')
    assert response.status_code == 200
    assert response.json() == {'db': 'ok', 'redis': 'ok'}


@pytest.mark.django_db
def test_healthz_returns_error_when_redis_is_down(
    client: Client, monkeypatch: pytest.MonkeyPatch
) -> None:
    def broken_set(*args: object, **kwargs: object) -> None:
        raise ConnectionError('redis unreachable')

    monkeypatch.setattr(cache, 'set', broken_set)
    response = client.get('/healthz')
    assert response.status_code == 503
    assert response.json() == {'db': 'ok', 'redis': 'error'}


@pytest.mark.django_db
def test_healthz_returns_error_when_db_is_down(
    client: Client, monkeypatch: pytest.MonkeyPatch
) -> None:
    def broken_cursor(*args: object, **kwargs: object) -> None:
        raise ConnectionError('db unreachable')

    monkeypatch.setattr(connection, 'cursor', broken_cursor)
    response = client.get('/healthz')
    assert response.status_code == 503
    assert response.json() == {'db': 'error', 'redis': 'ok'}
