from __future__ import annotations

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

STATUSES = ["DRAFT", "UNDER_REVIEW", "ACTIVE", "COMPLETED", "TERMINATED", "EXPIRED", "ARCHIVED"]

register(
    {
        "uz": {
            "contracts.new": "Yangi shartnoma",
            "contracts.search_placeholder": "Qidirish (raqam)",
            "contracts.col_number": "№",
            "contracts.col_client": "Mijoz",
            "contracts.col_status": "Holati",
            "contracts.col_amount": "Summa",
            "contracts.col_currency": "Valyuta",
            "contracts.total_line": "Jami: {n} ta",
            "contracts.client_id_input": "Mijoz ID *",
            "contracts.case_id_input": "Ish ID (ixtiyoriy)",
            "contracts.start_date_input": "Boshlanish sanasi (YYYY-MM-DD)",
            "contracts.end_date_input": "Tugash sanasi (YYYY-MM-DD)",
            "contracts.client_id_required": "Mijoz ID majburiy",
            "contracts.created": "Shartnoma yaratildi",
            "contracts.title_line": "Shartnoma № {number}",
            "contracts.amount_line": "Summa: {amount} {currency}",
            "contracts.term_line": "Muddat: {start} — {end}",
            "contracts.change_status_label": "Holatni o'zgartirish",
            "contracts.save_status": "Holatni saqlash",
            "contracts.status_updated": "Holat yangilandi",
            "contracts.attached_docs": "Biriktirilgan hujjatlar: {n}",
            "contracts.deleted": "Shartnoma o'chirildi",
            "status.DRAFT": "Qoralama",
            "status.UNDER_REVIEW": "Ko'rib chiqilmoqda",
            "status.ACTIVE": "Faol",
            "status.COMPLETED": "Yakunlangan",
            "status.TERMINATED": "Tugatilgan",
            "status.EXPIRED": "Muddati o'tgan",
            "status.ARCHIVED": "Arxivlangan",
        },
        "ru": {
            "contracts.new": "Новый договор",
            "contracts.search_placeholder": "Поиск (номер)",
            "contracts.col_number": "№",
            "contracts.col_client": "Клиент",
            "contracts.col_status": "Статус",
            "contracts.col_amount": "Сумма",
            "contracts.col_currency": "Валюта",
            "contracts.total_line": "Всего: {n}",
            "contracts.client_id_input": "ID клиента *",
            "contracts.case_id_input": "ID дела (необязательно)",
            "contracts.start_date_input": "Дата начала (YYYY-MM-DD)",
            "contracts.end_date_input": "Дата окончания (YYYY-MM-DD)",
            "contracts.client_id_required": "ID клиента обязателен",
            "contracts.created": "Договор создан",
            "contracts.title_line": "Договор № {number}",
            "contracts.amount_line": "Сумма: {amount} {currency}",
            "contracts.term_line": "Срок: {start} — {end}",
            "contracts.change_status_label": "Изменить статус",
            "contracts.save_status": "Сохранить статус",
            "contracts.status_updated": "Статус обновлён",
            "contracts.attached_docs": "Прикреплённые документы: {n}",
            "contracts.deleted": "Договор удалён",
            "status.DRAFT": "Черновик",
            "status.UNDER_REVIEW": "На рассмотрении",
            "status.ACTIVE": "Активен",
            "status.COMPLETED": "Завершён",
            "status.TERMINATED": "Прекращён",
            "status.EXPIRED": "Истёк",
            "status.ARCHIVED": "В архиве",
        },
        "en": {
            "contracts.new": "New contract",
            "contracts.search_placeholder": "Search (number)",
            "contracts.col_number": "No.",
            "contracts.col_client": "Client",
            "contracts.col_status": "Status",
            "contracts.col_amount": "Amount",
            "contracts.col_currency": "Currency",
            "contracts.total_line": "Total: {n}",
            "contracts.client_id_input": "Client ID *",
            "contracts.case_id_input": "Case ID (optional)",
            "contracts.start_date_input": "Start date (YYYY-MM-DD)",
            "contracts.end_date_input": "End date (YYYY-MM-DD)",
            "contracts.client_id_required": "Client ID is required",
            "contracts.created": "Contract created",
            "contracts.title_line": "Contract No. {number}",
            "contracts.amount_line": "Amount: {amount} {currency}",
            "contracts.term_line": "Term: {start} — {end}",
            "contracts.change_status_label": "Change status",
            "contracts.save_status": "Save status",
            "contracts.status_updated": "Status updated",
            "contracts.attached_docs": "Attached documents: {n}",
            "contracts.deleted": "Contract deleted",
            "status.DRAFT": "Draft",
            "status.UNDER_REVIEW": "Under review",
            "status.ACTIVE": "Active",
            "status.COMPLETED": "Completed",
            "status.TERMINATED": "Terminated",
            "status.EXPIRED": "Expired",
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
        {"name": "number", "label": t("contracts.col_number"), "field": "number", "align": "left"},
        {"name": "client_name", "label": t("contracts.col_client"), "field": "client_name", "align": "left"},
        {"name": "status", "label": t("contracts.col_status"), "field": "status", "align": "left"},
        {"name": "amount", "label": t("contracts.col_amount"), "field": "amount", "align": "right"},
        {"name": "currency", "label": t("contracts.col_currency"), "field": "currency", "align": "left"},
    ]

    with shell(active="/contracts"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label(t("nav.contracts")).classes("text-2xl font-bold")
            btn = ui.button(t("contracts.new"), icon="add", on_click=lambda: _open_create_dialog(reload))
            btn.props("unelevated color=primary")
            btn.set_visibility(state.has_permission("contracts.create"))

        search = ui.input(t("contracts.search_placeholder")).props("outlined dense clearable").classes("w-full")
        table = ui.table(columns=columns, rows=[], row_key="id").classes("w-full sp-card").props("flat bordered")
        table.on("rowClick", lambda e: _open_detail_dialog(e.args[1]["id"], reload))
        info_row = ui.row().classes("items-center justify-between w-full")

        async def reload() -> None:
            try:
                result = await state.client().list_("contracts", {"page": 1, "limit": 50, "search": search.value})
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            items = result.get("items", [])
            for it in items:
                it["client_name"] = (it.get("client") or {}).get("full_name", "")
            table.rows = items
            info_row.clear()
            with info_row:
                ui.label(t("contracts.total_line").format(n=result.get("meta", {}).get("total", 0)))

        search.on("keydown.enter", reload)
        ui.timer(0.05, reload, once=True)


def _open_create_dialog(on_saved) -> None:
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:420px;"):
        ui.label(t("contracts.new")).classes("text-lg font-bold")
        client_id = ui.input(t("contracts.client_id_input")).props("outlined dense").classes("w-full")
        case_id = ui.input(t("contracts.case_id_input")).props("outlined dense").classes("w-full")
        amount = ui.number(t("contracts.col_amount")).props("outlined dense").classes("w-full")
        currency = ui.input(t("contracts.col_currency"), value="UZS").props("outlined dense").classes("w-full")
        start_date = ui.input(t("contracts.start_date_input")).props("outlined dense").classes("w-full")
        end_date = ui.input(t("contracts.end_date_input")).props("outlined dense").classes("w-full")
        err = ui.label("").classes("text-negative text-caption")

        async def save() -> None:
            if not client_id.value:
                err.text = t("contracts.client_id_required")
                return
            payload = {
                "client_id": client_id.value,
                "case_id": case_id.value or None,
                "amount": amount.value,
                "currency": currency.value or "UZS",
                "start_date": start_date.value or None,
                "end_date": end_date.value or None,
            }
            try:
                await state.client().create("contracts", payload)
            except ApiError as exc:
                err.text = exc.message
                return
            ui.notify(t("contracts.created"), type="positive")
            dialog.close()
            await on_saved()

        with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
            ui.button(t("common.cancel"), on_click=dialog.close).props("flat")
            ui.button(t("common.save"), on_click=save).props("unelevated color=primary")
    dialog.open()


def _open_detail_dialog(contract_id: str, on_changed) -> None:
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:560px; max-width:720px;"):
        content = ui.column().classes("w-full gap-2")
        with content:
            ui.spinner()

        async def load() -> None:
            try:
                data = await state.client().get("contracts", contract_id)
            except ApiError as exc:
                content.clear()
                with content:
                    ui.label(exc.message).classes("text-negative")
                return
            content.clear()
            with content:
                with ui.row().classes("items-center justify-between w-full"):
                    ui.label(t("contracts.title_line").format(number=data.get("number", ""))).classes("text-xl font-bold")
                    ui.badge(_status_label(data.get("status", ""))).classes("q-px-sm")
                client = data.get("client") or {}
                ui.label(f"{t('contracts.col_client')}: {client.get('full_name', '—')}")
                ui.label(
                    t("contracts.amount_line").format(
                        amount=data.get("amount") or "—", currency=data.get("currency") or ""
                    )
                )
                ui.label(
                    t("contracts.term_line").format(
                        start=data.get("start_date") or "—", end=data.get("end_date") or "—"
                    )
                )

                if state.has_permission("contracts.update"):
                    ui.separator().classes("q-my-sm")
                    status_select = ui.select(STATUSES, value=data.get("status"), label=t("contracts.change_status_label")).props(
                        "outlined dense"
                    ).classes("w-full")

                    async def change_status() -> None:
                        try:
                            await state.client().update("contracts", contract_id, {"status": status_select.value})
                        except ApiError as exc:
                            ui.notify(exc.message, type="negative")
                            return
                        ui.notify(t("contracts.status_updated"), type="positive")
                        await load()

                    ui.button(t("contracts.save_status"), on_click=change_status).props("flat color=primary")

                docs = data.get("documents") or []
                ui.separator().classes("q-my-sm")
                ui.label(t("contracts.attached_docs").format(n=len(docs))).classes("text-caption sp-muted")

                with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
                    if state.has_permission("contracts.delete"):
                        async def remove() -> None:
                            try:
                                await state.client().delete("contracts", contract_id)
                            except ApiError as exc:
                                ui.notify(exc.message, type="negative")
                                return
                            ui.notify(t("contracts.deleted"), type="positive")
                            dialog.close()
                            await on_changed()

                        ui.button(t("common.delete"), on_click=remove).props("flat color=negative")
                    ui.button(t("common.close"), on_click=dialog.close).props("flat")

        ui.timer(0.05, load, once=True)
    dialog.open()
