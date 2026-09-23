from __future__ import annotations

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

register(
    {
        "uz": {
            "offices.address": "Manzil",
            "offices.region": "Viloyat",
            "offices.new": "Yangi ofis",
            "offices.edit_title": "Ofisni tahrirlash",
            "offices.new_title": "Yangi ofis",
            "offices.name_required": "Nomi va viloyat majburiy",
            "offices.deleted": "Ofis o'chirildi",
            "offices.saved": "Saqlandi",
            "offices.total": "Jami: {n} ta",
        },
        "ru": {
            "offices.address": "Адрес",
            "offices.region": "Регион",
            "offices.new": "Новый офис",
            "offices.edit_title": "Редактировать офис",
            "offices.new_title": "Новый офис",
            "offices.name_required": "Название и регион обязательны",
            "offices.deleted": "Офис удалён",
            "offices.saved": "Сохранено",
            "offices.total": "Всего: {n}",
        },
        "en": {
            "offices.address": "Address",
            "offices.region": "Region",
            "offices.new": "New office",
            "offices.edit_title": "Edit office",
            "offices.new_title": "New office",
            "offices.name_required": "Name and region are required",
            "offices.deleted": "Office deleted",
            "offices.saved": "Saved",
            "offices.total": "Total: {n}",
        },
    }
)


def render() -> None:
    if not require_login():
        return

    columns = [
        {"name": "name", "label": t("common.name"), "field": "name", "align": "left"},
        {"name": "address", "label": t("offices.address"), "field": "address", "align": "left"},
        {"name": "region_name", "label": t("offices.region"), "field": "region_name", "align": "left"},
    ]

    with shell(active="/offices"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label(t("nav.offices")).classes("text-2xl font-bold")
            can_manage = state.has_permission("offices.manage")
            add_btn = ui.button(t("offices.new"), icon="add", on_click=lambda: _open_form_dialog(None, reload))
            add_btn.props("unelevated color=indigo-7")
            add_btn.set_visibility(can_manage)

        table = ui.table(columns=columns, rows=[], row_key="id").classes("w-full sp-card").props("flat bordered")
        info_row = ui.row().classes("items-center justify-between w-full")

        if can_manage:
            table.on("rowClick", lambda e: _open_form_dialog(e.args[1], reload))

        async def reload() -> None:
            try:
                result = await state.client().list_("offices", {})
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            items = result if isinstance(result, list) else result.get("items", [])
            for it in items:
                it["region_name"] = (it.get("region") or {}).get("name", "—")
            table.rows = items
            info_row.clear()
            with info_row:
                ui.label(t("offices.total").format(n=len(items)))

        ui.timer(0.05, reload, once=True)


def _open_form_dialog(office: dict | None, on_saved) -> None:
    is_edit = office is not None
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:420px;"):
        ui.label(t("offices.edit_title") if is_edit else t("offices.new_title")).classes("text-lg font-bold")
        name = ui.input(f"{t('common.name')} *", value=(office or {}).get("name", "")).props("outlined dense").classes("w-full")
        address = ui.input(t("offices.address"), value=(office or {}).get("address") or "").props("outlined dense").classes("w-full")
        region_select = ui.select({}, label=f"{t('offices.region')} *").props("outlined dense").classes("w-full")
        err = ui.label("").classes("text-red-6 text-caption")

        async def load_regions() -> None:
            try:
                regions_result = await state.client().list_("regions", {})
            except ApiError as exc:
                err.text = exc.message
                return
            regions = regions_result if isinstance(regions_result, list) else regions_result.get("items", [])
            region_select.set_options({r["id"]: r["name"] for r in regions})
            if is_edit:
                region_select.value = (office or {}).get("region_id")

        async def save() -> None:
            if not name.value or not region_select.value:
                err.text = t("offices.name_required")
                return
            payload = {
                "name": name.value,
                "address": address.value or None,
                "region_id": region_select.value,
            }
            try:
                if is_edit:
                    await state.client().update("offices", office["id"], payload)
                else:
                    await state.client().create("offices", payload)
            except ApiError as exc:
                err.text = exc.message
                return
            ui.notify(t("offices.saved"), type="positive")
            dialog.close()
            await on_saved()

        async def remove() -> None:
            try:
                await state.client().delete("offices", office["id"])
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            ui.notify(t("offices.deleted"), type="positive")
            dialog.close()
            await on_saved()

        with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
            if is_edit and state.has_permission("offices.manage"):
                ui.button(t("common.delete"), on_click=remove).props("flat color=red")
            ui.button(t("common.cancel"), on_click=dialog.close).props("flat")
            ui.button(t("common.save"), on_click=save).props("unelevated color=indigo-7")

        ui.timer(0.05, load_regions, once=True)
    dialog.open()
