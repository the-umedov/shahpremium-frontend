from __future__ import annotations

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

STATUSES = ["DRAFT", "NEW", "OPEN", "IN_PROGRESS", "WAITING", "ON_HOLD", "CLOSED", "COMPLETED", "CANCELLED", "ARCHIVED"]
PRIORITIES = ["LOW", "NORMAL", "HIGH", "URGENT"]

register(
    {
        "uz": {
            "cases.new": "Yangi ish",
            "cases.search_placeholder": "Qidirish (raqam, sarlavha)",
            "cases.col_number": "№",
            "cases.col_title": "Sarlavha",
            "cases.col_client": "Mijoz",
            "cases.col_status": "Holati",
            "cases.col_priority": "Muhimlik",
            "cases.total_line": "Jami: {n} ta",
            "cases.title_input": "Sarlavha *",
            "cases.client_id_input": "Mijoz ID *",
            "cases.description": "Tavsif",
            "cases.case_type": "Ish turi",
            "cases.title_client_required": "Sarlavha va mijoz ID majburiy",
            "cases.created": "Ish yaratildi",
            "cases.change_status_label": "Holatni o'zgartirish",
            "cases.save_status": "Holatni saqlash",
            "cases.status_updated": "Holat yangilandi",
            "cases.notes_title": "Eslatmalar",
            "cases.no_notes": "Eslatmalar yo'q",
            "cases.new_note_input": "Yangi eslatma",
            "cases.add": "Qo'shish",
            "cases.deleted": "Ish o'chirildi",
            "status.DRAFT": "Qoralama",
            "status.NEW": "Yangi",
            "status.OPEN": "Ochiq",
            "status.IN_PROGRESS": "Jarayonda",
            "status.WAITING": "Kutilmoqda",
            "status.ON_HOLD": "To'xtatilgan",
            "status.CLOSED": "Yopilgan",
            "status.COMPLETED": "Yakunlangan",
            "status.CANCELLED": "Bekor qilingan",
            "status.ARCHIVED": "Arxivlangan",
        },
        "ru": {
            "cases.new": "Новое дело",
            "cases.search_placeholder": "Поиск (номер, заголовок)",
            "cases.col_number": "№",
            "cases.col_title": "Заголовок",
            "cases.col_client": "Клиент",
            "cases.col_status": "Статус",
            "cases.col_priority": "Приоритет",
            "cases.total_line": "Всего: {n}",
            "cases.title_input": "Заголовок *",
            "cases.client_id_input": "ID клиента *",
            "cases.description": "Описание",
            "cases.case_type": "Тип дела",
            "cases.title_client_required": "Заголовок и ID клиента обязательны",
            "cases.created": "Дело создано",
            "cases.change_status_label": "Изменить статус",
            "cases.save_status": "Сохранить статус",
            "cases.status_updated": "Статус обновлён",
            "cases.notes_title": "Заметки",
            "cases.no_notes": "Нет заметок",
            "cases.new_note_input": "Новая заметка",
            "cases.add": "Добавить",
            "cases.deleted": "Дело удалено",
            "status.DRAFT": "Черновик",
            "status.NEW": "Новое",
            "status.OPEN": "Открыто",
            "status.IN_PROGRESS": "В процессе",
            "status.WAITING": "Ожидание",
            "status.ON_HOLD": "Приостановлено",
            "status.CLOSED": "Закрыто",
            "status.COMPLETED": "Завершено",
            "status.CANCELLED": "Отменено",
            "status.ARCHIVED": "В архиве",
        },
        "en": {
            "cases.new": "New case",
            "cases.search_placeholder": "Search (number, title)",
            "cases.col_number": "No.",
            "cases.col_title": "Title",
            "cases.col_client": "Client",
            "cases.col_status": "Status",
            "cases.col_priority": "Priority",
            "cases.total_line": "Total: {n}",
            "cases.title_input": "Title *",
            "cases.client_id_input": "Client ID *",
            "cases.description": "Description",
            "cases.case_type": "Case type",
            "cases.title_client_required": "Title and client ID are required",
            "cases.created": "Case created",
            "cases.change_status_label": "Change status",
            "cases.save_status": "Save status",
            "cases.status_updated": "Status updated",
            "cases.notes_title": "Notes",
            "cases.no_notes": "No notes",
            "cases.new_note_input": "New note",
            "cases.add": "Add",
            "cases.deleted": "Case deleted",
            "status.DRAFT": "Draft",
            "status.NEW": "New",
            "status.OPEN": "Open",
            "status.IN_PROGRESS": "In progress",
            "status.WAITING": "Waiting",
            "status.ON_HOLD": "On hold",
            "status.CLOSED": "Closed",
            "status.COMPLETED": "Completed",
            "status.CANCELLED": "Cancelled",
            "status.ARCHIVED": "Archived",
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
        {"name": "number", "label": t("cases.col_number"), "field": "number", "align": "left"},
        {"name": "title", "label": t("cases.col_title"), "field": "title", "align": "left"},
        {"name": "client_name", "label": t("cases.col_client"), "field": "client_name", "align": "left"},
        {"name": "status", "label": t("cases.col_status"), "field": "status", "align": "left"},
        {"name": "priority", "label": t("cases.col_priority"), "field": "priority", "align": "left"},
    ]

    with shell(active="/cases"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label(t("nav.cases")).classes("text-2xl font-bold")
            btn = ui.button(t("cases.new"), icon="add", on_click=lambda: _open_create_dialog(reload))
            btn.props("unelevated color=primary")
            btn.set_visibility(state.has_permission("cases.create"))

        search = ui.input(t("cases.search_placeholder")).props("outlined dense clearable").classes("w-full")
        table = ui.table(columns=columns, rows=[], row_key="id").classes("w-full sp-card").props("flat bordered")
        table.on("rowClick", lambda e: _open_detail_dialog(e.args[1]["id"], reload))
        info_row = ui.row().classes("items-center justify-between w-full")

        async def reload() -> None:
            try:
                result = await state.client().list_("cases", {"page": 1, "limit": 50, "search": search.value})
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            items = result.get("items", [])
            for it in items:
                it["client_name"] = (it.get("client") or {}).get("full_name", "")
            table.rows = items
            info_row.clear()
            with info_row:
                ui.label(t("cases.total_line").format(n=result.get("meta", {}).get("total", 0)))

        search.on("keydown.enter", reload)
        ui.timer(0.05, reload, once=True)


def _open_create_dialog(on_saved) -> None:
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:420px;"):
        ui.label(t("cases.new")).classes("text-lg font-bold")
        title = ui.input(t("cases.title_input")).props("outlined dense").classes("w-full")
        client_id = ui.input(t("cases.client_id_input")).props("outlined dense").classes("w-full")
        description = ui.textarea(t("cases.description")).props("outlined dense").classes("w-full")
        case_type = ui.input(t("cases.case_type")).props("outlined dense").classes("w-full")
        priority = ui.select(PRIORITIES, value="NORMAL", label=t("cases.col_priority")).props("outlined dense").classes("w-full")
        err = ui.label("").classes("text-negative text-caption")

        async def save() -> None:
            if not title.value or not client_id.value:
                err.text = t("cases.title_client_required")
                return
            payload = {
                "title": title.value,
                "client_id": client_id.value,
                "description": description.value or None,
                "case_type": case_type.value or None,
                "priority": priority.value,
            }
            try:
                await state.client().create("cases", payload)
            except ApiError as exc:
                err.text = exc.message
                return
            ui.notify(t("cases.created"), type="positive")
            dialog.close()
            await on_saved()

        with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
            ui.button(t("common.cancel"), on_click=dialog.close).props("flat")
            ui.button(t("common.save"), on_click=save).props("unelevated color=primary")
    dialog.open()


def _open_detail_dialog(case_id: str, on_changed) -> None:
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:560px; max-width:720px;"):
        content = ui.column().classes("w-full gap-2")
        with content:
            ui.spinner()

        async def load() -> None:
            try:
                data = await state.client().get("cases", case_id)
            except ApiError as exc:
                content.clear()
                with content:
                    ui.label(exc.message).classes("text-negative")
                return
            content.clear()
            with content:
                with ui.row().classes("items-center justify-between w-full"):
                    ui.label(data.get("title", "")).classes("text-xl font-bold")
                    ui.badge(_status_label(data.get("status", ""))).classes("q-px-sm")
                ui.label(f"{t('cases.col_number')} {data.get('number', '')}").classes("text-caption sp-muted")
                client = data.get("client") or {}
                ui.label(f"{t('cases.col_client')}: {client.get('full_name', '—')}")
                ui.label(f"{t('cases.description')}: {data.get('description') or '—'}")

                if state.has_permission("cases.update"):
                    ui.separator().classes("q-my-sm")
                    status_select = ui.select(STATUSES, value=data.get("status"), label=t("cases.change_status_label")).props(
                        "outlined dense"
                    ).classes("w-full")

                    async def change_status() -> None:
                        try:
                            await state.client().update("cases", case_id, {"status": status_select.value})
                        except ApiError as exc:
                            ui.notify(exc.message, type="negative")
                            return
                        ui.notify(t("cases.status_updated"), type="positive")
                        await load()

                    ui.button(t("cases.save_status"), on_click=change_status).props("flat color=primary")

                ui.separator().classes("q-my-sm")
                ui.label(t("cases.notes_title")).classes("text-md font-semibold")
                notes = data.get("notes") or []
                if not notes:
                    ui.label(t("cases.no_notes")).classes("text-caption sp-subtle")
                for n in notes[:10]:
                    ui.label(f"• {n.get('body', '')}").classes("text-sm")

                if state.has_permission("cases.update"):
                    with ui.row().classes("w-full items-end gap-2"):
                        note_body = ui.input(t("cases.new_note_input")).props("outlined dense").classes("col")

                        async def add_note() -> None:
                            if not note_body.value:
                                return
                            try:
                                await state.client().add_case_note(case_id, note_body.value)
                            except ApiError as exc:
                                ui.notify(exc.message, type="negative")
                                return
                            note_body.value = ""
                            await load()

                        ui.button(t("cases.add"), on_click=add_note).props("flat color=primary")

                with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
                    if state.has_permission("cases.delete"):
                        async def remove() -> None:
                            try:
                                await state.client().delete("cases", case_id)
                            except ApiError as exc:
                                ui.notify(exc.message, type="negative")
                                return
                            ui.notify(t("cases.deleted"), type="positive")
                            dialog.close()
                            await on_changed()

                        ui.button(t("common.delete"), on_click=remove).props("flat color=negative")
                    ui.button(t("common.close"), on_click=dialog.close).props("flat")

        ui.timer(0.05, load, once=True)
    dialog.open()
