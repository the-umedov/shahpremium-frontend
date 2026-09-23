from __future__ import annotations

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

register(
    {
        "uz": {
            "permissions.no_access": "Ushbu bo'limni ko'rish uchun ruxsatingiz yo'q",
            "permissions.search": "Qidirish (kalit, resurs, amal)",
            "permissions.resource": "Resurs",
            "permissions.all": "Barchasi",
            "permissions.col.key": "Kalit",
            "permissions.col.resource": "Resurs",
            "permissions.col.action": "Amal",
            "permissions.col.description": "Tavsif",
        },
        "ru": {
            "permissions.no_access": "У вас нет прав для просмотра этого раздела",
            "permissions.search": "Поиск (ключ, ресурс, действие)",
            "permissions.resource": "Ресурс",
            "permissions.all": "Все",
            "permissions.col.key": "Ключ",
            "permissions.col.resource": "Ресурс",
            "permissions.col.action": "Действие",
            "permissions.col.description": "Описание",
        },
        "en": {
            "permissions.no_access": "You do not have permission to view this section",
            "permissions.search": "Search (key, resource, action)",
            "permissions.resource": "Resource",
            "permissions.all": "All",
            "permissions.col.key": "Key",
            "permissions.col.resource": "Resource",
            "permissions.col.action": "Action",
            "permissions.col.description": "Description",
        },
    }
)


def render() -> None:
    if not require_login():
        return

    columns = [
        {"name": "key", "label": t("permissions.col.key"), "field": "key", "align": "left"},
        {"name": "resource", "label": t("permissions.col.resource"), "field": "resource", "align": "left"},
        {"name": "action", "label": t("permissions.col.action"), "field": "action", "align": "left"},
        {"name": "description", "label": t("permissions.col.description"), "field": "description", "align": "left"},
    ]

    with shell(active="/permissions"):
        ui.label(t("nav.permissions")).classes("text-2xl font-bold")

        if not state.has_permission("roles.manage"):
            ui.label(t("permissions.no_access")).classes("text-negative")
            return

        with ui.row().classes("w-full items-end gap-2"):
            search = ui.input(t("permissions.search")).props("outlined dense clearable").classes("w-full")
            resource_filter = ui.select({"": t("permissions.all")}, value="", label=t("permissions.resource")).props(
                "outlined dense"
            ).classes("w-56")

        table = ui.table(columns=columns, rows=[], row_key="id").classes("w-full sp-card").props("flat bordered")
        info_row = ui.row().classes("items-center justify-between w-full")

        all_permissions: list[dict] = []

        def apply_filters() -> None:
            q = (search.value or "").strip().lower()
            res = resource_filter.value
            rows = all_permissions
            if res:
                rows = [p for p in rows if p.get("resource") == res]
            if q:
                rows = [
                    p for p in rows
                    if q in (p.get("key") or "").lower()
                    or q in (p.get("resource") or "").lower()
                    or q in (p.get("action") or "").lower()
                ]
            table.rows = rows
            info_row.clear()
            with info_row:
                ui.label(f"{t('common.total')}: {len(rows)}")

        async def load() -> None:
            nonlocal all_permissions
            try:
                all_permissions = await state.client().list_("permissions")
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            resources = sorted({p.get("resource") for p in all_permissions if p.get("resource")})
            options = {"": t("permissions.all")}
            options.update({r: r for r in resources})
            resource_filter.set_options(options)
            apply_filters()

        search.on("keydown.enter", apply_filters)
        resource_filter.on_value_change(apply_filters)
        ui.timer(0.05, load, once=True)
