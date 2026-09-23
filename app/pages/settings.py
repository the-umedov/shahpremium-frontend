from __future__ import annotations

import json

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import LOCALE_LABELS, register, t
from app.shell import require_login, shell

THEMES = ["system", "light", "dark"]

register(
    {
        "uz": {
            "settings.mine": "Mening sozlamalarim",
            "settings.system": "Tizim sozlamalari",
            "settings.locale": "Til",
            "settings.theme": "Mavzu",
            "settings.timezone": "Vaqt mintaqasi",
            "settings.date_format": "Sana formati",
            "settings.notifications": "Bildirishnomalar",
            "settings.notify_in_app": "Ilova ichida",
            "settings.notify_email": "Email",
            "settings.notify_sms": "SMS",
            "settings.notify_push": "Push",
            "settings.saved": "Sozlamalar saqlandi",
            "settings.kv_title": "Global kalit/qiymat sozlamalari",
            "settings.kv_new": "Yangi sozlama",
            "settings.kv_none": "Sozlamalar yo'q",
            "settings.kv_edit_title": "Sozlamani tahrirlash",
            "settings.kv_key": "Kalit (key) *",
            "settings.kv_value": "Qiymat (JSON)",
            "settings.kv_key_required": "Kalit majburiy",
            "settings.kv_invalid_json": "Qiymat to'g'ri JSON bo'lishi kerak",
        },
        "ru": {
            "settings.mine": "Мои настройки",
            "settings.system": "Системные настройки",
            "settings.locale": "Язык",
            "settings.theme": "Тема",
            "settings.timezone": "Часовой пояс",
            "settings.date_format": "Формат даты",
            "settings.notifications": "Уведомления",
            "settings.notify_in_app": "В приложении",
            "settings.notify_email": "Email",
            "settings.notify_sms": "SMS",
            "settings.notify_push": "Push",
            "settings.saved": "Настройки сохранены",
            "settings.kv_title": "Глобальные настройки ключ/значение",
            "settings.kv_new": "Новая настройка",
            "settings.kv_none": "Нет настроек",
            "settings.kv_edit_title": "Редактировать настройку",
            "settings.kv_key": "Ключ (key) *",
            "settings.kv_value": "Значение (JSON)",
            "settings.kv_key_required": "Ключ обязателен",
            "settings.kv_invalid_json": "Значение должно быть корректным JSON",
        },
        "en": {
            "settings.mine": "My preferences",
            "settings.system": "System settings",
            "settings.locale": "Language",
            "settings.theme": "Theme",
            "settings.timezone": "Timezone",
            "settings.date_format": "Date format",
            "settings.notifications": "Notifications",
            "settings.notify_in_app": "In-app",
            "settings.notify_email": "Email",
            "settings.notify_sms": "SMS",
            "settings.notify_push": "Push",
            "settings.saved": "Settings saved",
            "settings.kv_title": "Global key/value settings",
            "settings.kv_new": "New setting",
            "settings.kv_none": "No settings",
            "settings.kv_edit_title": "Edit setting",
            "settings.kv_key": "Key *",
            "settings.kv_value": "Value (JSON)",
            "settings.kv_key_required": "Key is required",
            "settings.kv_invalid_json": "Value must be valid JSON",
        },
    }
)


def render() -> None:
    if not require_login():
        return

    with shell(active="/settings"):
        ui.label(t("nav.settings")).classes("text-2xl font-bold")

        ui.label(t("settings.mine")).classes("text-lg font-semibold q-mt-md")
        _render_preferences_section()

        if state.has_permission("settings.manage"):
            ui.separator().classes("q-my-md")
            ui.label(t("settings.system")).classes("text-lg font-semibold")
            _render_system_settings_section()


def _render_preferences_section() -> None:
    form_col = ui.column().classes("w-full gap-2 sp-card q-pa-md")

    async def load() -> None:
        try:
            pref = await state.client().get_preferences()
        except ApiError as exc:
            ui.notify(exc.message, type="negative")
            return
        # Backend — saqlangan qiymatning haqiqiy manbasi; brauzer-holatini
        # shu bilan sinxronlaymiz (masalan yangi qurilmada birinchi kirishda).
        state.set_locale(pref.get("locale", "uz"))
        state.set_theme(pref.get("theme", "system"))

        form_col.clear()
        with form_col:
            with ui.row().classes("w-full gap-4"):
                locale = ui.select(LOCALE_LABELS, value=pref.get("locale", "uz"), label=t("settings.locale")).props(
                    "outlined dense"
                ).classes("col")
                theme = ui.select(
                    {key: t(f"theme.{key}") for key in THEMES}, value=pref.get("theme", "system"), label=t("settings.theme")
                ).props(
                    "outlined dense"
                ).classes("col")
                timezone = ui.input(t("settings.timezone"), value=pref.get("timezone", "Asia/Tashkent")).props(
                    "outlined dense"
                ).classes("col")
                date_format = ui.input(
                    t("settings.date_format"), value=pref.get("date_format", "dd.MM.yyyy")
                ).props("outlined dense").classes("col")
            ui.label(t("settings.notifications")).classes("font-medium q-mt-sm")
            with ui.row().classes("gap-6"):
                notify_in_app = ui.switch(t("settings.notify_in_app"), value=pref.get("notify_in_app", True))
                notify_email = ui.switch(t("settings.notify_email"), value=pref.get("notify_email", True))
                notify_sms = ui.switch(t("settings.notify_sms"), value=pref.get("notify_sms", False))
                notify_push = ui.switch(t("settings.notify_push"), value=pref.get("notify_push", False))
            err = ui.label("").classes("text-negative text-caption")

            async def save() -> None:
                payload = {
                    "locale": locale.value,
                    "theme": theme.value,
                    "timezone": timezone.value,
                    "date_format": date_format.value,
                    "notify_in_app": notify_in_app.value,
                    "notify_email": notify_email.value,
                    "notify_sms": notify_sms.value,
                    "notify_push": notify_push.value,
                }
                try:
                    await state.client().update_preferences(payload)
                except ApiError as exc:
                    err.text = exc.message
                    return
                err.text = ""
                state.set_locale(locale.value)
                state.set_theme(theme.value)
                ui.notify(t("settings.saved"), type="positive")
                # Til matnlari va tema render vaqtida baholanadi — o'zgarishni
                # butun sahifada qo'llash uchun to'liq qayta yuklaymiz.
                ui.navigate.reload()

            ui.button(t("common.save"), on_click=save).props("unelevated color=primary").classes("q-mt-sm")

    ui.timer(0.05, load, once=True)


def _render_system_settings_section() -> None:
    with ui.row().classes("w-full items-center justify-between"):
        ui.label(t("settings.kv_title")).classes("text-md")
        ui.button(
            t("settings.kv_new"), icon="add", on_click=lambda: _open_setting_dialog(None, reload)
        ).props("unelevated color=primary")

    list_col = ui.column().classes("w-full gap-1")

    async def reload() -> None:
        try:
            items = await state.client().list_settings_kv()
        except ApiError as exc:
            ui.notify(exc.message, type="negative")
            return
        list_col.clear()
        with list_col:
            if not items:
                ui.label(t("settings.kv_none")).classes("text-caption sp-subtle")
            for s in items:
                with ui.row().classes(
                    "w-full items-center justify-between sp-card q-pa-sm cursor-pointer"
                ).on("click", lambda i=s: _open_setting_dialog(i, reload)):
                    with ui.column().classes("gap-0"):
                        ui.label(s.get("key", "")).classes("font-medium")
                        ui.label(json.dumps(s.get("value"), ensure_ascii=False)[:80]).classes(
                            "text-caption sp-muted"
                        )
                    ui.badge(s.get("scope", "GLOBAL"))

    ui.timer(0.05, reload, once=True)


def _open_setting_dialog(item: dict | None, on_saved) -> None:
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:480px;"):
        ui.label(t("settings.kv_edit_title") if item else t("settings.kv_new")).classes("text-lg font-bold")
        key = ui.input(t("settings.kv_key"), value=(item or {}).get("key", "")).props("outlined dense").classes("w-full")
        if item:
            key.props("readonly")
        scope = ui.input("Scope", value=(item or {}).get("scope", "GLOBAL")).props("outlined dense").classes(
            "w-full"
        )
        value_text = json.dumps((item or {}).get("value", ""), ensure_ascii=False, indent=2) if item else "{}"
        value = ui.textarea(t("settings.kv_value"), value=value_text).props("outlined dense").classes("w-full").style(
            "font-family:monospace;"
        )
        err = ui.label("").classes("text-negative text-caption")

        async def save() -> None:
            if not key.value:
                err.text = t("settings.kv_key_required")
                return
            try:
                parsed_value = json.loads(value.value) if value.value.strip() else None
            except json.JSONDecodeError:
                err.text = t("settings.kv_invalid_json")
                return
            payload = {"key": key.value, "value": parsed_value, "scope": scope.value or None}
            try:
                await state.client().upsert_setting(payload)
            except ApiError as exc:
                err.text = exc.message
                return
            ui.notify(t("settings.saved"), type="positive")
            dialog.close()
            await on_saved()

        with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
            ui.button(t("common.cancel"), on_click=dialog.close).props("flat")
            ui.button(t("common.save"), on_click=save).props("unelevated color=primary")
    dialog.open()
