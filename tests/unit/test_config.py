from core.config import get_settings


def test_get_settings() -> None:
    settings = get_settings()
    assert settings.app_name
    assert settings.port > 0
