from __future__ import annotations

import json

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

INTEGRATION_TYPES = ["PAYMENT", "EMAIL", "SMS", "MAPS", "CALENDAR", "EXTERNAL_ORG", "ACCOUNTING", "EDMS"]
PARTNER_STATUSES = ["ACTIVE", "INACTIVE", "SUSPENDED"]

register(
    {
        "uz": {
            "integrations.forbidden": "Bu sahifa uchun ruxsatingiz yo'q",
            "integrations.tab_partners": "Hamkor tashkilotlar",
            "integrations.connected_title": "Ulangan integratsiyalar",
            "integrations.new": "Yangi integratsiya",
            "integrations.empty": "Hozircha integratsiyalar yo'q",
            "integrations.updated": "Yangilandi",
            "integrations.edit_title": "Integratsiyani tahrirlash",
            "integrations.key_label": "Kalit (key) *",
            "integrations.name_label": "Nomi *",
            "integrations.type_label": "Turi",
            "integrations.enabled_label": "Yoqilgan",
            "integrations.config_label": "Konfiguratsiya (JSON)",
            "integrations.key_name_required": "Kalit va nomi majburiy",
            "integrations.invalid_json": "Konfiguratsiya to'g'ri JSON bo'lishi kerak",
            "integrations.saved": "Saqlandi",
            "integrations.new_partner": "Yangi hamkor",
            "integrations.partners_empty": "Hozircha hamkor tashkilotlar yo'q",
            "integrations.contract_label": "Shartnoma: {value}",
            "integrations.partner_deleted": "Hamkor o'chirildi",
            "integrations.edit_partner_title": "Hamkorni tahrirlash",
            "integrations.new_partner_title": "Yangi hamkor tashkilot",
            "integrations.description_label": "Tavsif",
            "integrations.contract_number_label": "Shartnoma raqami",
            "integrations.services_label": "Xizmatlar (vergul bilan)",
            "integrations.name_required": "Nomi majburiy",
            "status.PAYMENT": "To'lov",
            "status.EMAIL": "Email",
            "status.SMS": "SMS",
            "status.MAPS": "Xaritalar",
            "status.CALENDAR": "Kalendar",
            "status.EXTERNAL_ORG": "Tashqi tashkilot",
            "status.ACCOUNTING": "Buxgalteriya",
            "status.EDMS": "Elektron hujjat aylanishi",
            "status.ACTIVE": "Faol",
            "status.INACTIVE": "Nofaol",
            "status.SUSPENDED": "To'xtatilgan",
        },
        "ru": {
            "integrations.forbidden": "У вас нет доступа к этой странице",
            "integrations.tab_partners": "Партнёрские организации",
            "integrations.connected_title": "Подключённые интеграции",
            "integrations.new": "Новая интеграция",
            "integrations.empty": "Интеграций пока нет",
            "integrations.updated": "Обновлено",
            "integrations.edit_title": "Редактировать интеграцию",
            "integrations.key_label": "Ключ (key) *",
            "integrations.name_label": "Название *",
            "integrations.type_label": "Тип",
            "integrations.enabled_label": "Включено",
            "integrations.config_label": "Конфигурация (JSON)",
            "integrations.key_name_required": "Ключ и название обязательны",
            "integrations.invalid_json": "Конфигурация должна быть корректным JSON",
            "integrations.saved": "Сохранено",
            "integrations.new_partner": "Новый партнёр",
            "integrations.partners_empty": "Партнёрских организаций пока нет",
            "integrations.contract_label": "Договор: {value}",
            "integrations.partner_deleted": "Партнёр удалён",
            "integrations.edit_partner_title": "Редактировать партнёра",
            "integrations.new_partner_title": "Новая партнёрская организация",
            "integrations.description_label": "Описание",
            "integrations.contract_number_label": "Номер договора",
            "integrations.services_label": "Услуги (через запятую)",
            "integrations.name_required": "Название обязательно",
            "status.PAYMENT": "Платежи",
            "status.EMAIL": "Email",
            "status.SMS": "SMS",
            "status.MAPS": "Карты",
            "status.CALENDAR": "Календарь",
            "status.EXTERNAL_ORG": "Внешняя организация",
            "status.ACCOUNTING": "Бухгалтерия",
            "status.EDMS": "Электронный документооборот",
            "status.ACTIVE": "Активен",
            "status.INACTIVE": "Неактивен",
            "status.SUSPENDED": "Приостановлен",
        },
        "en": {
            "integrations.forbidden": "You don't have permission to view this page",
            "integrations.tab_partners": "Partner organizations",
            "integrations.connected_title": "Connected integrations",
            "integrations.new": "New integration",
            "integrations.empty": "No integrations yet",
            "integrations.updated": "Updated",
            "integrations.edit_title": "Edit integration",
            "integrations.key_label": "Key *",
            "integrations.name_label": "Name *",
            "integrations.type_label": "Type",
            "integrations.enabled_label": "Enabled",
            "integrations.config_label": "Configuration (JSON)",
            "integrations.key_name_required": "Key and name are required",
            "integrations.invalid_json": "Configuration must be valid JSON",
            "integrations.saved": "Saved",
            "integrations.new_partner": "New partner",
            "integrations.partners_empty": "No partner organizations yet",
            "integrations.contract_label": "Contract: {value}",
            "integrations.partner_deleted": "Partner deleted",
            "integrations.edit_partner_title": "Edit partner",
            "integrations.new_partner_title": "New partner organization",
            "integrations.description_label": "Description",
            "integrations.contract_number_label": "Contract number",
            "integrations.services_label": "Services (comma-separated)",
            "integrations.name_required": "Name is required",
            "status.PAYMENT": "Payment",
            "status.EMAIL": "Email",
            "status.SMS": "SMS",
            "status.MAPS": "Maps",
            "status.CALENDAR": "Calendar",
            "status.EXTERNAL_ORG": "External organization",
            "status.ACCOUNTING": "Accounting",
            "status.EDMS": "Electronic document management",
            "status.ACTIVE": "Active",
            "status.INACTIVE": "Inactive",
            "status.SUSPENDED": "Suspended",
        },
    }
)


def render() -> None:
    if not require_login():
        return

    with shell(active="/integrations"):
        if not state.has_permission("integrations.manage"):
            ui.label(t("integrations.forbidden")).classes("text-red-6")
            return

        ui.label(t("nav.integrations")).classes("text-2xl font-bold")

        tabs = ui.tabs().classes("w-full")
        with tabs:
            tab_integrations = ui.tab(t("nav.integrations"))
            tab_partners = ui.tab(t("integrations.tab_partners"))

        with ui.tab_panels(tabs, value=tab_integrations).classes("w-full"):
            with ui.tab_panel(tab_integrations):
                _render_integrations_panel()
            with ui.tab_panel(tab_partners):
                _render_partners_panel()


def _render_integrations_panel() -> None:
    with ui.row().classes("w-full items-center justify-between"):
        ui.label(t("integrations.connected_title")).classes("text-lg font-semibold")
        ui.button(
            t("integrations.new"), icon="add", on_click=lambda: _open_integration_dialog(None, reload)
        ).props("unelevated color=indigo-7")

    list_col = ui.column().classes("w-full gap-2")

    async def reload() -> None:
        try:
            items = await state.client().list_integrations()
        except ApiError as exc:
            ui.notify(exc.message, type="negative")
            return
        list_col.clear()
        with list_col:
            if not items:
                ui.label(t("integrations.empty")).classes("text-caption text-grey-5")
            for it in items:
                with ui.row().classes("w-full items-center justify-between sp-card q-pa-sm"):
                    with ui.column().classes("gap-0"):
                        ui.label(f"{it.get('name')} ({it.get('key')})").classes("font-medium")
                        ui.label(t(f"status.{it['type']}") if it.get("type") else "—").classes(
                            "text-caption text-grey-6"
                        )
                    with ui.row().classes("items-center gap-2"):
                        ui.switch(
                            value=bool(it.get("is_enabled")),
                            on_change=lambda e, i=it: _toggle_enabled(i, e.value, reload),
                        )
                        ui.button(icon="edit", on_click=lambda i=it: _open_integration_dialog(i, reload)).props(
                            "flat dense round"
                        )

    ui.timer(0.05, reload, once=True)


async def _toggle_enabled(item: dict, new_value: bool, on_changed) -> None:
    payload = {
        "key": item["key"],
        "name": item["name"],
        "type": item.get("type"),
        "is_enabled": new_value,
        "config": item.get("config"),
    }
    try:
        await state.client().upsert_integration(payload)
    except ApiError as exc:
        ui.notify(exc.message, type="negative")
        await on_changed()
        return
    ui.notify(t("integrations.updated"), type="positive")
    await on_changed()


def _open_integration_dialog(item: dict | None, on_saved) -> None:
    type_options = {v: t(f"status.{v}") for v in INTEGRATION_TYPES}
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:480px;"):
        ui.label(t("integrations.edit_title") if item else t("integrations.new")).classes("text-lg font-bold")
        key = ui.input(t("integrations.key_label"), value=(item or {}).get("key", "")).props(
            "outlined dense"
        ).classes("w-full")
        if item:
            key.props("readonly")
        name = ui.input(t("integrations.name_label"), value=(item or {}).get("name", "")).props(
            "outlined dense"
        ).classes("w-full")
        itype = ui.select(type_options, value=(item or {}).get("type"), label=t("integrations.type_label")).props(
            "outlined dense clearable"
        ).classes("w-full")
        is_enabled = ui.switch(t("integrations.enabled_label"), value=bool((item or {}).get("is_enabled")))
        config_text = json.dumps((item or {}).get("config") or {}, ensure_ascii=False, indent=2)
        config = ui.textarea(t("integrations.config_label"), value=config_text).props("outlined dense").classes(
            "w-full"
        ).style("font-family:monospace;")
        err = ui.label("").classes("text-red-6 text-caption")

        async def save() -> None:
            if not key.value or not name.value:
                err.text = t("integrations.key_name_required")
                return
            try:
                config_value = json.loads(config.value) if config.value.strip() else {}
            except json.JSONDecodeError:
                err.text = t("integrations.invalid_json")
                return
            payload = {
                "key": key.value,
                "name": name.value,
                "type": itype.value,
                "is_enabled": is_enabled.value,
                "config": config_value,
            }
            try:
                await state.client().upsert_integration(payload)
            except ApiError as exc:
                err.text = exc.message
                return
            ui.notify(t("integrations.saved"), type="positive")
            dialog.close()
            await on_saved()

        with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
            ui.button(t("common.cancel"), on_click=dialog.close).props("flat")
            ui.button(t("common.save"), on_click=save).props("unelevated color=indigo-7")
    dialog.open()


def _render_partners_panel() -> None:
    with ui.row().classes("w-full items-center justify-between"):
        ui.label(t("integrations.tab_partners")).classes("text-lg font-semibold")
        ui.button(t("integrations.new_partner"), icon="add", on_click=lambda: _open_partner_dialog(None, reload)).props(
            "unelevated color=indigo-7"
        )

    list_col = ui.column().classes("w-full gap-2")

    async def reload() -> None:
        try:
            items = await state.client().list_partners()
        except ApiError as exc:
            ui.notify(exc.message, type="negative")
            return
        list_col.clear()
        with list_col:
            if not items:
                ui.label(t("integrations.partners_empty")).classes("text-caption text-grey-5")
            for p in items:
                with ui.row().classes("w-full items-center justify-between sp-card q-pa-sm"):
                    with ui.column().classes("gap-0"):
                        with ui.row().classes("items-center gap-2"):
                            ui.label(p.get("name", "")).classes("font-medium")
                            ui.badge(t(f"status.{p['status']}") if p.get("status") else "").classes("q-px-sm")
                        ui.label(p.get("description") or "—").classes("text-caption text-grey-6")
                        if p.get("contract_number"):
                            ui.label(t("integrations.contract_label").format(value=p["contract_number"])).classes(
                                "text-caption text-grey-6"
                            )
                    with ui.row().classes("items-center gap-2"):
                        ui.button(icon="edit", on_click=lambda i=p: _open_partner_dialog(i, reload)).props(
                            "flat dense round"
                        )
                        ui.button(
                            icon="delete", on_click=lambda i=p: _remove_partner(i["id"], reload)
                        ).props("flat dense round color=red")

    ui.timer(0.05, reload, once=True)


async def _remove_partner(partner_id: str, on_changed) -> None:
    try:
        await state.client().delete_partner(partner_id)
    except ApiError as exc:
        ui.notify(exc.message, type="negative")
        return
    ui.notify(t("integrations.partner_deleted"), type="positive")
    await on_changed()


def _open_partner_dialog(item: dict | None, on_saved) -> None:
    status_options = {v: t(f"status.{v}") for v in PARTNER_STATUSES}
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:480px;"):
        ui.label(t("integrations.edit_partner_title") if item else t("integrations.new_partner_title")).classes(
            "text-lg font-bold"
        )
        name = ui.input(t("integrations.name_label"), value=(item or {}).get("name", "")).props(
            "outlined dense"
        ).classes("w-full")
        description = ui.textarea(t("integrations.description_label"), value=(item or {}).get("description", "")).props(
            "outlined dense"
        ).classes("w-full")
        contract_number = ui.input(
            t("integrations.contract_number_label"), value=(item or {}).get("contract_number", "")
        ).props("outlined dense").classes("w-full")
        services_val = ", ".join((item or {}).get("services") or [])
        services = ui.input(t("integrations.services_label"), value=services_val).props("outlined dense").classes(
            "w-full"
        )
        status = ui.select(
            status_options, value=(item or {}).get("status", "ACTIVE"), label=t("common.status")
        ).props("outlined dense").classes("w-full")
        err = ui.label("").classes("text-red-6 text-caption")

        async def save() -> None:
            if not name.value:
                err.text = t("integrations.name_required")
                return
            payload = {
                "name": name.value,
                "description": description.value or None,
                "contract_number": contract_number.value or None,
                "services": [s.strip() for s in services.value.split(",") if s.strip()],
                "status": status.value,
            }
            try:
                if item:
                    await state.client().update_partner(item["id"], payload)
                else:
                    await state.client().create_partner(payload)
            except ApiError as exc:
                err.text = exc.message
                return
            ui.notify(t("integrations.saved"), type="positive")
            dialog.close()
            await on_saved()

        with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
            ui.button(t("common.cancel"), on_click=dialog.close).props("flat")
            ui.button(t("common.save"), on_click=save).props("unelevated color=indigo-7")
    dialog.open()
