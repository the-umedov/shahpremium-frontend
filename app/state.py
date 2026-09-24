"""Brauzer-sessiya darajasidagi holat (NiceGUI app.storage.user asosida)."""

from __future__ import annotations

from nicegui import app

from app.api_client import ApiClient


def get_token() -> str | None:
    return app.storage.user.get("access_token")


def set_session(*, access_token: str, me: dict) -> None:
    app.storage.user["access_token"] = access_token
    app.storage.user["me"] = me


def clear_session() -> None:
    app.storage.user.pop("access_token", None)
    app.storage.user.pop("me", None)


def get_me() -> dict | None:
    return app.storage.user.get("me")


def is_authenticated() -> bool:
    return bool(get_token())


def is_client() -> bool:
    """CLIENT rolidagi foydalanuvchi — unga menyu va boshqaruv paneli boshqacha ko'rsatiladi."""
    me = get_me() or {}
    return "CLIENT" in (me.get("roles") or [])


def get_drawer_mini() -> bool:
    return bool(app.storage.user.get("drawer_mini", False))


def set_drawer_mini(mini: bool) -> None:
    app.storage.user["drawer_mini"] = mini


def has_permission(perm: str) -> bool:
    me = get_me() or {}
    granted = set(me.get("permissions") or [])
    if perm in granted:
        return True
    resource = perm.split(".")[0]
    return f"{resource}.manage" in granted


def client() -> ApiClient:
    return ApiClient(access_token=get_token())


# ---- til / mavzu (i18n + theme) ----
# Brauzer-sessiyasida saqlanadi (app.storage.user, storage_secret bilan
# cookie orqali) — backenddagi UserPreference bilan settings sahifasi
# orqali sinxronlanadi, lekin darhol UI javob berishi uchun mustaqil.

DEFAULT_LOCALE = "uz"
DEFAULT_THEME = "system"


def get_locale() -> str:
    return app.storage.user.get("locale", DEFAULT_LOCALE)


def set_locale(locale: str) -> None:
    app.storage.user["locale"] = locale


def get_theme() -> str:
    """'light' | 'dark' | 'system'."""
    return app.storage.user.get("theme", DEFAULT_THEME)


def set_theme(theme: str) -> None:
    app.storage.user["theme"] = theme
