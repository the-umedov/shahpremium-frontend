from __future__ import annotations

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

register(
    {
        "uz": {
            "regions.title": "Viloyatlar",
            "regions.code": "Kod",
            "regions.offices_count": "Ofislar",
            "regions.clients_count": "Mijozlar",
            "regions.new": "Yangi viloyat",
            "regions.edit_title": "Viloyatni tahrirlash",
            "regions.new_title": "Yangi viloyat",
            "regions.name_required": "Nomi va kod majburiy",
            "regions.deleted": "Viloyat o'chirildi",
            "regions.saved": "Saqlandi",
            "regions.total": "Jami: {n} ta",
        },
        "ru": {
            "regions.title": "Регионы",
            "regions.code": "Код",
            "regions.offices_count": "Офисы",
            "regions.clients_count": "Клиенты",
            "regions.new": "Новый регион",
            "regions.edit_title": "Редактировать регион",
            "regions.new_title": "Новый регион",
            "regions.name_required": "Название и код обязательны",
            "regions.deleted": "Регион удалён",
            "regions.saved": "Сохранено",
            "regions.total": "Всего: {n}",
        },
        "en": {
            "regions.title": "Regions",
            "regions.code": "Code",
            "regions.offices_count": "Offices",
            "regions.clients_count": "Clients",
            "regions.new": "New region",
            "regions.edit_title": "Edit region",
            "regions.new_title": "New region",
            "regions.name_required": "Name and code are required",
            "regions.deleted": "Region deleted",
            "regions.saved": "Saved",
            "regions.total": "Total: {n}",
        },
    }
)


def render() -> None:
    if not require_login():
        return

    columns = [
        {"name": "code", "label": t("regions.code"), "field": "code", "align": "left"},
        {"name": "name", "label": t("common.name"), "field": "name", "align": "left"},
        {"name": "offices_count", "label": t("regions.offices_count"), "field": "offices_count", "align": "right"},
        {"name": "clients_count", "label": t("regions.clients_count"), "field": "clients_count", "align": "right"},
    ]

    with shell(active="/regions"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label(t("nav.regions")).classes("text-2xl font-bold")
            can_manage = state.has_permission("regions.manage")
            add_btn = ui.button(t("regions.new"), icon="add", on_click=lambda: _open_form_dialog(None, reload))
            add_btn.props("unelevated color=indigo-7")
            add_btn.set_visibility(can_manage)

        table = ui.table(columns=columns, rows=[], row_key="id").classes("w-full sp-card").props("flat bordered")
        info_row = ui.row().classes("items-center justify-between w-full")

        if can_manage:
            table.on("rowClick", lambda e: _open_form_dialog(e.args[1], reload))

        async def reload() -> None:
            try:
                result = await state.client().list_("regions", {})
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            items = result if isinstance(result, list) else result.get("items", [])
            for it in items:
                count = it.get("count") or {}
                it["offices_count"] = count.get("offices", 0)
                it["clients_count"] = count.get("clients", 0)
            table.rows = items
            info_row.clear()
            with info_row:
                ui.label(t("regions.total").format(n=len(items)))

        ui.timer(0.05, reload, once=True)


def _open_form_dialog(region: dict | None, on_saved) -> None:
    is_edit = region is not None
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:380px;"):
        ui.label(t("regions.edit_title") if is_edit else t("regions.new_title")).classes("text-lg font-bold")
        name = ui.input(f"{t('common.name')} *", value=(region or {}).get("name", "")).props("outlined dense").classes("w-full")
        code = ui.input(f"{t('regions.code')} *", value=(region or {}).get("code", "")).props("outlined dense").classes("w-full")
        err = ui.label("").classes("text-red-6 text-caption")

        async def save() -> None:
            if not name.value or not code.value:
                err.text = t("regions.name_required")
                return
            payload = {"name": name.value, "code": code.value}
            try:
                if is_edit:
                    await state.client().update("regions", region["id"], payload)
                else:
                    await state.client().create("regions", payload)
            except ApiError as exc:
                err.text = exc.message
                return
            ui.notify(t("regions.saved"), type="positive")
            dialog.close()
            await on_saved()

        async def remove() -> None:
            try:
                await state.client().delete("regions", region["id"])
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            ui.notify(t("regions.deleted"), type="positive")
            dialog.close()
            await on_saved()

        with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
            if is_edit and state.has_permission("regions.manage"):
                ui.button(t("common.delete"), on_click=remove).props("flat color=red")
            ui.button(t("common.cancel"), on_click=dialog.close).props("flat")
            ui.button(t("common.save"), on_click=save).props("unelevated color=indigo-7")
    dialog.open()
