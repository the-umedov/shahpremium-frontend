from __future__ import annotations

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

register(
    {
        "uz": {"dashboard.welcome": "Xush kelibsiz", "dashboard.roles": "rollar", "dashboard.no_roles": "yo'q"},
        "ru": {"dashboard.welcome": "С возвращением", "dashboard.roles": "роли", "dashboard.no_roles": "нет"},
        "en": {"dashboard.welcome": "Welcome back", "dashboard.roles": "roles", "dashboard.no_roles": "none"},
    }
)


def render() -> None:
    if not require_login():
        return
    me = state.get_me() or {}

    with shell(active="/"):
        ui.label(t("nav.dashboard")).classes("text-2xl font-bold")
        roles = ", ".join(me.get("roles") or []) or t("dashboard.no_roles")
        ui.label(f"{t('dashboard.welcome')} — {t('dashboard.roles')}: {roles}").classes("text-grey-7")

        cards = ui.row().classes("gap-4 w-full")
        with cards:
            _stat_card(t("nav.clients"), "clients", "clients.read", "groups")
            _stat_card(t("nav.cases"), "cases", "cases.read", "gavel")
            _stat_card(t("nav.contracts"), "contracts", "contracts.read", "description")
            _stat_card(t("nav.documents"), "documents", "documents.read", "folder")


def _stat_card(label: str, resource: str, perm: str, icon: str) -> None:
    with ui.card().classes("sp-card q-pa-md").style("min-width:180px;"):
        ui.icon(icon).classes("text-3xl text-indigo-600")
        ui.label(label).classes("text-grey-7 text-sm")
        value_label = ui.label("…").classes("text-2xl font-bold")

        async def load() -> None:
            if not state.has_permission(perm):
                value_label.text = "—"
                return
            try:
                page = await state.client().list_(resource, {"page": 1, "limit": 1})
                value_label.text = str(page.get("meta", {}).get("total", "—"))
            except ApiError:
                value_label.text = "—"
            except Exception:
                value_label.text = "—"

        ui.timer(0.05, load, once=True)
