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
            "regions.districts_count": "Tumanlar",
            "regions.districts_title": "Tumanlar",
            "regions.no_districts": "Tumanlar kiritilmagan",
            "regions.new_district": "Yangi tuman nomi",
            "regions.district_added": "Tuman qo'shildi",
            "regions.district_removed": "Tuman o'chirildi",
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
            "regions.districts_count": "Районы",
            "regions.districts_title": "Районы",
            "regions.no_districts": "Районы не добавлены",
            "regions.new_district": "Название нового района",
            "regions.district_added": "Район добавлен",
            "regions.district_removed": "Район удалён",
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
            "regions.districts_count": "Districts",
            "regions.districts_title": "Districts",
            "regions.no_districts": "No districts added",
            "regions.new_district": "New district name",
            "regions.district_added": "District added",
            "regions.district_removed": "District removed",
        },
    }
)


def render() -> None:
    if not require_login():
        return

    columns = [
        {"name": "code", "label": t("regions.code"), "field": "code", "align": "left"},
        {"name": "name", "label": t("common.name"), "field": "name", "align": "left"},
        {"name": "districts_count", "label": t("regions.districts_count"), "field": "districts_count", "align": "right"},
        {"name": "offices_count", "label": t("regions.offices_count"), "field": "offices_count", "align": "right"},
        {"name": "clients_count", "label": t("regions.clients_count"), "field": "clients_count", "align": "right"},
    ]

    with shell(active="/regions"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label(t("nav.regions")).classes("text-2xl font-bold")
            can_manage = state.has_permission("regions.manage")
            add_btn = ui.button(t("regions.new"), icon="add", on_click=lambda: _open_form_dialog(None, reload))
            add_btn.props("unelevated color=primary")
            add_btn.set_visibility(can_manage)

        table = ui.table(columns=columns, rows=[], row_key="id").classes("w-full sp-card cursor-pointer").props(
            "flat bordered :rows-per-page-options='[0]' hide-pagination"
        )
        info_row = ui.row().classes("items-center justify-between w-full")
        by_id: dict[str, dict] = {}

        # Tumanlarni hamma ko'ra oladi; tahrirlash faqat regions.manage bilan.
        table.on("rowClick", lambda e: _open_form_dialog(by_id.get(e.args[1]["id"], e.args[1]), reload))

        async def reload() -> None:
            try:
                result = await state.client().list_("regions", {})
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            items = result if isinstance(result, list) else result.get("items", [])
            by_id.clear()
            for it in items:
                count = it.get("count") or {}
                it["offices_count"] = count.get("offices", 0)
                it["clients_count"] = count.get("clients", 0)
                it["districts_count"] = count.get("districts", 0)
                by_id[it["id"]] = it
            # Jadval satrlarida tumanlar ro'yxatini tashimaymiz (175 ta yozuv) — dialog by_id'dan oladi.
            table.rows = [{k: v for k, v in it.items() if k != "districts"} for it in items]
            info_row.clear()
            with info_row:
                ui.label(t("regions.total").format(n=len(items)))

        ui.timer(0.05, reload, once=True)


def _open_form_dialog(region: dict | None, on_saved) -> None:
    is_edit = region is not None
    can_manage = state.has_permission("regions.manage")
    readonly = "" if can_manage else " readonly"
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:420px; max-width:640px;"):
        title = (region or {}).get("name") if is_edit and not can_manage else (
            t("regions.edit_title") if is_edit else t("regions.new_title")
        )
        ui.label(title).classes("text-lg font-bold")
        name = ui.input(f"{t('common.name')} *", value=(region or {}).get("name", "")).props(
            f"outlined dense{readonly}"
        ).classes("w-full")
        code = ui.input(f"{t('regions.code')} *", value=(region or {}).get("code", "")).props(
            f"outlined dense{readonly}"
        ).classes("w-full")
        err = ui.label("").classes("text-negative text-caption")

        if is_edit:
            _districts_section(region, can_manage, on_saved)

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
            if not can_manage:
                ui.button(t("common.close"), on_click=dialog.close).props("flat")
            else:
                if is_edit:
                    ui.button(t("common.delete"), on_click=remove).props("flat color=negative")
                ui.button(t("common.cancel"), on_click=dialog.close).props("flat")
                ui.button(t("common.save"), on_click=save).props("unelevated color=primary")
    dialog.open()


def _districts_section(region: dict, can_manage: bool, on_saved) -> None:
    ui.label(t("regions.districts_title")).classes("font-medium q-mt-sm")
    chips_box = ui.row().classes("w-full gap-1 flex-wrap").style("max-height:260px; overflow-y:auto;")

    async def remove_district(district: dict) -> None:
        try:
            updated = await state.client().remove_district(region["id"], district["id"])
        except ApiError as exc:
            ui.notify(exc.message, type="negative")
            return
        ui.notify(t("regions.district_removed"), type="positive")
        draw(updated.get("districts", []))
        await on_saved()

    def draw(districts: list[dict]) -> None:
        region["districts"] = districts
        chips_box.clear()
        with chips_box:
            if not districts:
                ui.label(t("regions.no_districts")).classes("sp-subtle text-caption")
            for d in districts:
                ui.chip(
                    d["name"],
                    removable=can_manage,
                    on_value_change=lambda e, d=d: remove_district(d) if not e.value else None,
                ).props("outline color=primary dense")

    draw(region.get("districts") or [])

    if can_manage:
        with ui.row().classes("w-full items-center gap-2 no-wrap"):
            new_name = ui.input(t("regions.new_district")).props("outlined dense").classes("col")

            async def add() -> None:
                value = (new_name.value or "").strip()
                if not value:
                    return
                try:
                    updated = await state.client().add_district(region["id"], value)
                except ApiError as exc:
                    ui.notify(exc.message, type="negative")
                    return
                new_name.value = ""
                ui.notify(t("regions.district_added"), type="positive")
                draw(updated.get("districts", []))
                await on_saved()

            ui.button(icon="add", on_click=add).props("unelevated round dense color=primary")
            new_name.on("keydown.enter", add)
