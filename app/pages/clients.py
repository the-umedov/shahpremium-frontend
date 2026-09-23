from __future__ import annotations

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

CLIENT_TYPES = ["INDIVIDUAL", "ORGANIZATION"]  # haqiqiy baza: ClientType enum

register(
    {
        "uz": {
            "clients.new": "Yangi mijoz",
            "clients.search_placeholder": "Qidirish (ism, telefon, email, kod)",
            "clients.col_code": "Kod",
            "clients.col_full_name": "F.I.Sh. / Nomi",
            "clients.col_type": "Turi",
            "clients.col_phone": "Telefon",
            "clients.col_email": "Email",
            "clients.total_line": "Jami: {n} ta",
            "clients.full_name_input": "F.I.Sh. / Tashkilot nomi *",
            "clients.address": "Manzil",
            "clients.tax_id": "STIR / INN",
            "clients.full_name_required": "F.I.Sh. / nomi majburiy",
            "clients.created": "Mijoz yaratildi",
            "clients.total_paid": "Jami to'langan",
            "clients.history_title": "Tarix (timeline)",
            "clients.no_history": "Hozircha yozuvlar yo'q",
            "clients.new_note_label": "Yangi eslatma sarlavhasi",
            "clients.add": "Qo'shish",
            "clients.deleted": "Mijoz o'chirildi",
            "status.INDIVIDUAL": "Jismoniy shaxs",
            "status.ORGANIZATION": "Yuridik shaxs",
        },
        "ru": {
            "clients.new": "Новый клиент",
            "clients.search_placeholder": "Поиск (имя, телефон, email, код)",
            "clients.col_code": "Код",
            "clients.col_full_name": "ФИО / Название",
            "clients.col_type": "Тип",
            "clients.col_phone": "Телефон",
            "clients.col_email": "Email",
            "clients.total_line": "Всего: {n}",
            "clients.full_name_input": "ФИО / Название организации *",
            "clients.address": "Адрес",
            "clients.tax_id": "ИНН",
            "clients.full_name_required": "ФИО / название обязательно",
            "clients.created": "Клиент создан",
            "clients.total_paid": "Всего оплачено",
            "clients.history_title": "История (таймлайн)",
            "clients.no_history": "Пока нет записей",
            "clients.new_note_label": "Заголовок новой заметки",
            "clients.add": "Добавить",
            "clients.deleted": "Клиент удалён",
            "status.INDIVIDUAL": "Физическое лицо",
            "status.ORGANIZATION": "Юридическое лицо",
        },
        "en": {
            "clients.new": "New client",
            "clients.search_placeholder": "Search (name, phone, email, code)",
            "clients.col_code": "Code",
            "clients.col_full_name": "Full name / Name",
            "clients.col_type": "Type",
            "clients.col_phone": "Phone",
            "clients.col_email": "Email",
            "clients.total_line": "Total: {n}",
            "clients.full_name_input": "Full name / Organization name *",
            "clients.address": "Address",
            "clients.tax_id": "Tax ID",
            "clients.full_name_required": "Full name / name is required",
            "clients.created": "Client created",
            "clients.total_paid": "Total paid",
            "clients.history_title": "History (timeline)",
            "clients.no_history": "No entries yet",
            "clients.new_note_label": "New note title",
            "clients.add": "Add",
            "clients.deleted": "Client deleted",
            "status.INDIVIDUAL": "Individual",
            "status.ORGANIZATION": "Organization",
        },
    }
)


def _status_label(value: str) -> str:
    key = f"status.{value}"
    label = t(key)
    return value if label == key else label


def render() -> None:
    if not require_login():
        return

    columns = [
        {"name": "code", "label": t("clients.col_code"), "field": "code", "align": "left"},
        {"name": "full_name", "label": t("clients.col_full_name"), "field": "full_name", "align": "left"},
        {"name": "client_type", "label": t("clients.col_type"), "field": "client_type", "align": "left"},
        {"name": "phone", "label": t("clients.col_phone"), "field": "phone", "align": "left"},
        {"name": "email", "label": t("clients.col_email"), "field": "email", "align": "left"},
    ]

    with shell(active="/clients"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label(t("nav.clients")).classes("text-2xl font-bold")
            can_create = state.has_permission("clients.create")
            add_btn = ui.button(t("clients.new"), icon="add", on_click=lambda: _open_create_dialog(reload))
            add_btn.props("unelevated color=indigo-7")
            add_btn.set_visibility(can_create)

        search = ui.input(t("clients.search_placeholder")).props("outlined dense clearable").classes("w-full")
        table = ui.table(columns=columns, rows=[], row_key="id").classes("w-full sp-card").props("flat bordered")
        table.on("rowClick", lambda e: _open_detail_dialog(e.args[1]["id"], reload))
        pagination_row = ui.row().classes("items-center justify-between w-full")

        state_page = {"page": 1, "limit": 20, "total_pages": 1}

        async def reload() -> None:
            try:
                result = await state.client().list_(
                    "clients", {"page": state_page["page"], "limit": state_page["limit"], "search": search.value}
                )
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            items = result.get("items", [])
            for it in items:
                it["_id_short"] = (it.get("id") or "")[:8]
            table.rows = items
            meta = result.get("meta", {})
            state_page["total_pages"] = meta.get("total_pages", 1)
            pagination_row.clear()
            with pagination_row:
                ui.label(t("clients.total_line").format(n=meta.get("total", 0)))
                with ui.row().classes("items-center gap-2"):
                    ui.button(icon="chevron_left", on_click=lambda: _change_page(-1)).props("flat dense").bind_enabled_from(
                        state_page, "page", backward=lambda p: p > 1
                    )
                    ui.label(f"{state_page['page']} / {state_page['total_pages']}")
                    ui.button(icon="chevron_right", on_click=lambda: _change_page(1)).props("flat dense")

        async def _change_page(delta: int) -> None:
            new_page = state_page["page"] + delta
            if new_page < 1 or new_page > state_page["total_pages"]:
                return
            state_page["page"] = new_page
            await reload()

        search.on("keydown.enter", reload)
        ui.timer(0.05, reload, once=True)


def _open_create_dialog(on_saved) -> None:
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:420px;"):
        ui.label(t("clients.new")).classes("text-lg font-bold")
        full_name = ui.input(t("clients.full_name_input")).props("outlined dense").classes("w-full")
        client_type = ui.select(CLIENT_TYPES, value="INDIVIDUAL", label=t("clients.col_type")).props("outlined dense").classes("w-full")
        phone = ui.input(t("clients.col_phone")).props("outlined dense").classes("w-full")
        email = ui.input(t("clients.col_email")).props("outlined dense").classes("w-full")
        address = ui.textarea(t("clients.address")).props("outlined dense").classes("w-full")
        tax_id = ui.input(t("clients.tax_id")).props("outlined dense").classes("w-full")
        err = ui.label("").classes("text-red-6 text-caption")

        async def save() -> None:
            if not full_name.value:
                err.text = t("clients.full_name_required")
                return
            payload = {
                "full_name": full_name.value,
                "client_type": client_type.value,
                "phone": phone.value or None,
                "email": email.value or None,
                "address": address.value or None,
                "tax_id": tax_id.value or None,
            }
            try:
                await state.client().create("clients", payload)
            except ApiError as exc:
                err.text = exc.message
                return
            ui.notify(t("clients.created"), type="positive")
            dialog.close()
            await on_saved()

        with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
            ui.button(t("common.cancel"), on_click=dialog.close).props("flat")
            ui.button(t("common.save"), on_click=save).props("unelevated color=indigo-7")
    dialog.open()


def _open_detail_dialog(client_id: str, on_changed) -> None:
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:560px; max-width:720px;"):
        content = ui.column().classes("w-full gap-2")
        with content:
            ui.spinner()

        async def load() -> None:
            try:
                data = await state.client().get("clients", client_id)
            except ApiError as exc:
                content.clear()
                with content:
                    ui.label(exc.message).classes("text-red-6")
                return
            content.clear()
            with content:
                with ui.row().classes("items-center justify-between w-full"):
                    ui.label(data.get("full_name", "")).classes("text-xl font-bold")
                    ui.badge(_status_label(data.get("client_type", ""))).classes("q-px-sm")
                ui.label(f"{t('clients.col_code')}: {data.get('code', '')}").classes("text-caption text-grey-6")

                with ui.row().classes("gap-6 q-mt-sm"):
                    ui.label(f"{t('clients.col_phone')}: {data.get('phone') or '—'}")
                    ui.label(f"{t('clients.col_email')}: {data.get('email') or '—'}")
                ui.label(f"{t('clients.address')}: {data.get('address') or '—'}")
                ui.label(f"{t('clients.tax_id')}: {data.get('tax_id') or '—'}")

                stats = data.get("stats") or {}
                with ui.row().classes("gap-4 q-mt-md"):
                    for key, label in [
                        ("cases", t("nav.cases")), ("contracts", t("nav.contracts")),
                        ("documents", t("nav.documents")), ("payments", t("nav.payments")),
                    ]:
                        with ui.column().classes("items-center"):
                            ui.label(str(stats.get(key, 0))).classes("text-lg font-bold text-indigo-700")
                            ui.label(label).classes("text-caption text-grey-6")
                    with ui.column().classes("items-center"):
                        ui.label(f"{stats.get('total_paid', 0):,}").classes("text-lg font-bold text-green-700")
                        ui.label(t("clients.total_paid")).classes("text-caption text-grey-6")

                ui.separator().classes("q-my-sm")
                ui.label(t("clients.history_title")).classes("text-md font-semibold")
                timeline = data.get("timeline") or []
                if not timeline:
                    ui.label(t("clients.no_history")).classes("text-caption text-grey-5")
                for ev in timeline[:10]:
                    with ui.row().classes("items-start gap-2"):
                        ui.icon("fiber_manual_record").classes("text-xs text-indigo-400 q-mt-xs")
                        with ui.column().classes("gap-0"):
                            ui.label(ev.get("title", "")).classes("text-sm font-medium")
                            if ev.get("description"):
                                ui.label(ev["description"]).classes("text-caption text-grey-6")

                if state.has_permission("clients.update"):
                    ui.separator().classes("q-my-sm")
                    with ui.row().classes("w-full items-end gap-2"):
                        note_title = ui.input(t("clients.new_note_label")).props("outlined dense").classes("col")

                        async def add_note() -> None:
                            if not note_title.value:
                                return
                            try:
                                await state.client().add_client_note(client_id, note_title.value)
                            except ApiError as exc:
                                ui.notify(exc.message, type="negative")
                                return
                            note_title.value = ""
                            await load()

                        ui.button(t("clients.add"), on_click=add_note).props("flat color=indigo-7")

                with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
                    if state.has_permission("clients.delete"):
                        async def remove() -> None:
                            try:
                                await state.client().delete("clients", client_id)
                            except ApiError as exc:
                                ui.notify(exc.message, type="negative")
                                return
                            ui.notify(t("clients.deleted"), type="positive")
                            dialog.close()
                            await on_changed()

                        ui.button(t("common.delete"), on_click=remove).props("flat color=red")
                    ui.button(t("common.close"), on_click=dialog.close).props("flat")

        ui.timer(0.05, load, once=True)
    dialog.open()
