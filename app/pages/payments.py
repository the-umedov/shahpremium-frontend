from __future__ import annotations

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

DIRECTIONS = ["INCOME", "EXPENSE"]
CATEGORIES = ["SERVICES", "STATE_FEE", "POSTAL", "OTHER"]
METHODS = ["CASH", "CARD", "BANK_TRANSFER", "ONLINE"]
STATUSES = ["PENDING", "PAID", "PARTIAL", "REFUNDED", "FAILED", "CANCELLED"]

STATUS_COLORS = {
    "PENDING": "warning",
    "PAID": "positive",
    "PARTIAL": "info",
    "REFUNDED": "grey-7",
    "FAILED": "negative",
    "CANCELLED": "grey-8",
}

register(
    {
        "uz": {
            "payments.create": "Yangi to'lov",
            "payments.filter.all": "Barchasi",
            "payments.filter.direction": "Turi",
            "payments.filter.category": "Kategoriya",
            "payments.filter.date_from": "Sanadan (YYYY-MM-DD)",
            "payments.filter.date_to": "Sanagacha (YYYY-MM-DD)",
            "payments.filter.apply": "Filtrlash",
            "payments.summary.income": "Daromad",
            "payments.summary.expense": "Xarajat",
            "payments.summary.refunded": "Qaytarilgan",
            "payments.summary.profit": "Foyda",
            "payments.summary.debt": "Qarzdorlik",
            "payments.col.client": "Mijoz",
            "payments.col.direction": "Turi",
            "payments.col.category": "Kategoriya",
            "payments.col.amount": "Summa",
            "payments.col.currency": "Valyuta",
            "payments.create.title": "Yangi to'lov",
            "payments.create.client_search": "Mijozni qidirish",
            "payments.create.client": "Mijoz *",
            "payments.create.client_search_btn": "Mijozlarni qidirish",
            "payments.create.amount": "Summa *",
            "payments.create.currency": "Valyuta",
            "payments.create.direction": "Turi",
            "payments.create.category": "Kategoriya",
            "payments.create.method": "To'lov usuli",
            "payments.create.case_id": "Ish ID (ixtiyoriy)",
            "payments.create.contract_id": "Shartnoma ID (ixtiyoriy)",
            "payments.create.invoice_id": "Invoys ID (ixtiyoriy)",
            "payments.create.comment": "Izoh",
            "payments.err.select_client": "Mijozni tanlang",
            "payments.err.amount_required": "Summa majburiy",
            "payments.created": "To'lov yaratildi",
            "payments.detail.client": "Mijoz",
            "payments.detail.type": "Turi",
            "payments.detail.category": "Kategoriya",
            "payments.detail.method": "Usul",
            "payments.detail.case": "Ish",
            "payments.detail.contract": "Shartnoma",
            "payments.detail.comment": "Izoh",
            "payments.detail.paid_at": "To'langan sana",
            "payments.detail.change_status": "Holatni o'zgartirish",
            "payments.detail.save_status": "Holatni saqlash",
            "payments.detail.refund": "Qaytarish (refund)",
            "payments.status_updated": "Holat yangilandi",
            "payments.refunded_msg": "To'lov qaytarildi",
            "status.PENDING": "Kutilmoqda",
            "status.PAID": "To'langan",
            "status.PARTIAL": "Qisman to'langan",
            "status.REFUNDED": "Qaytarilgan",
            "status.FAILED": "Muvaffaqiyatsiz",
            "status.CANCELLED": "Bekor qilingan",
            "status.INCOME": "Daromad",
            "status.EXPENSE": "Xarajat",
            "status.SERVICES": "Xizmatlar",
            "status.STATE_FEE": "Davlat bojligi",
            "status.POSTAL": "Pochta",
            "status.OTHER": "Boshqa",
            "status.CASH": "Naqd",
            "status.CARD": "Karta",
            "status.BANK_TRANSFER": "Bank o'tkazmasi",
            "status.ONLINE": "Onlayn",
        },
        "ru": {
            "payments.create": "Новый платёж",
            "payments.filter.all": "Все",
            "payments.filter.direction": "Тип",
            "payments.filter.category": "Категория",
            "payments.filter.date_from": "С даты (YYYY-MM-DD)",
            "payments.filter.date_to": "По дату (YYYY-MM-DD)",
            "payments.filter.apply": "Отфильтровать",
            "payments.summary.income": "Доход",
            "payments.summary.expense": "Расход",
            "payments.summary.refunded": "Возвращено",
            "payments.summary.profit": "Прибыль",
            "payments.summary.debt": "Задолженность",
            "payments.col.client": "Клиент",
            "payments.col.direction": "Тип",
            "payments.col.category": "Категория",
            "payments.col.amount": "Сумма",
            "payments.col.currency": "Валюта",
            "payments.create.title": "Новый платёж",
            "payments.create.client_search": "Поиск клиента",
            "payments.create.client": "Клиент *",
            "payments.create.client_search_btn": "Искать клиентов",
            "payments.create.amount": "Сумма *",
            "payments.create.currency": "Валюта",
            "payments.create.direction": "Тип",
            "payments.create.category": "Категория",
            "payments.create.method": "Способ оплаты",
            "payments.create.case_id": "ID дела (необязательно)",
            "payments.create.contract_id": "ID договора (необязательно)",
            "payments.create.invoice_id": "ID счёта (необязательно)",
            "payments.create.comment": "Комментарий",
            "payments.err.select_client": "Выберите клиента",
            "payments.err.amount_required": "Сумма обязательна",
            "payments.created": "Платёж создан",
            "payments.detail.client": "Клиент",
            "payments.detail.type": "Тип",
            "payments.detail.category": "Категория",
            "payments.detail.method": "Способ",
            "payments.detail.case": "Дело",
            "payments.detail.contract": "Договор",
            "payments.detail.comment": "Комментарий",
            "payments.detail.paid_at": "Дата оплаты",
            "payments.detail.change_status": "Изменить статус",
            "payments.detail.save_status": "Сохранить статус",
            "payments.detail.refund": "Возврат (refund)",
            "payments.status_updated": "Статус обновлён",
            "payments.refunded_msg": "Платёж возвращён",
            "status.PENDING": "В ожидании",
            "status.PAID": "Оплачено",
            "status.PARTIAL": "Частично оплачено",
            "status.REFUNDED": "Возвращено",
            "status.FAILED": "Не удалось",
            "status.CANCELLED": "Отменено",
            "status.INCOME": "Доход",
            "status.EXPENSE": "Расход",
            "status.SERVICES": "Услуги",
            "status.STATE_FEE": "Госпошлина",
            "status.POSTAL": "Почта",
            "status.OTHER": "Другое",
            "status.CASH": "Наличные",
            "status.CARD": "Карта",
            "status.BANK_TRANSFER": "Банковский перевод",
            "status.ONLINE": "Онлайн",
        },
        "en": {
            "payments.create": "New payment",
            "payments.filter.all": "All",
            "payments.filter.direction": "Type",
            "payments.filter.category": "Category",
            "payments.filter.date_from": "From date (YYYY-MM-DD)",
            "payments.filter.date_to": "To date (YYYY-MM-DD)",
            "payments.filter.apply": "Filter",
            "payments.summary.income": "Income",
            "payments.summary.expense": "Expense",
            "payments.summary.refunded": "Refunded",
            "payments.summary.profit": "Profit",
            "payments.summary.debt": "Debt",
            "payments.col.client": "Client",
            "payments.col.direction": "Type",
            "payments.col.category": "Category",
            "payments.col.amount": "Amount",
            "payments.col.currency": "Currency",
            "payments.create.title": "New payment",
            "payments.create.client_search": "Search client",
            "payments.create.client": "Client *",
            "payments.create.client_search_btn": "Search clients",
            "payments.create.amount": "Amount *",
            "payments.create.currency": "Currency",
            "payments.create.direction": "Type",
            "payments.create.category": "Category",
            "payments.create.method": "Payment method",
            "payments.create.case_id": "Case ID (optional)",
            "payments.create.contract_id": "Contract ID (optional)",
            "payments.create.invoice_id": "Invoice ID (optional)",
            "payments.create.comment": "Comment",
            "payments.err.select_client": "Select a client",
            "payments.err.amount_required": "Amount is required",
            "payments.created": "Payment created",
            "payments.detail.client": "Client",
            "payments.detail.type": "Type",
            "payments.detail.category": "Category",
            "payments.detail.method": "Method",
            "payments.detail.case": "Case",
            "payments.detail.contract": "Contract",
            "payments.detail.comment": "Comment",
            "payments.detail.paid_at": "Paid at",
            "payments.detail.change_status": "Change status",
            "payments.detail.save_status": "Save status",
            "payments.detail.refund": "Refund",
            "payments.status_updated": "Status updated",
            "payments.refunded_msg": "Payment refunded",
            "status.PENDING": "Pending",
            "status.PAID": "Paid",
            "status.PARTIAL": "Partially paid",
            "status.REFUNDED": "Refunded",
            "status.FAILED": "Failed",
            "status.CANCELLED": "Cancelled",
            "status.INCOME": "Income",
            "status.EXPENSE": "Expense",
            "status.SERVICES": "Services",
            "status.STATE_FEE": "State fee",
            "status.POSTAL": "Postal",
            "status.OTHER": "Other",
            "status.CASH": "Cash",
            "status.CARD": "Card",
            "status.BANK_TRANSFER": "Bank transfer",
            "status.ONLINE": "Online",
        },
    }
)


def render() -> None:
    if not require_login():
        return

    columns = [
        {"name": "client_name", "label": t("payments.col.client"), "field": "client_name", "align": "left"},
        {"name": "direction", "label": t("payments.col.direction"), "field": "direction", "align": "left"},
        {"name": "category", "label": t("payments.col.category"), "field": "category", "align": "left"},
        {"name": "amount", "label": t("payments.col.amount"), "field": "amount", "align": "right"},
        {"name": "currency", "label": t("payments.col.currency"), "field": "currency", "align": "left"},
        {"name": "status", "label": t("common.status"), "field": "status", "align": "left"},
    ]

    with shell(active="/payments"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label(t("nav.payments")).classes("text-2xl font-bold")
            add_btn = ui.button(t("payments.create"), icon="add", on_click=lambda: _open_create_dialog(reload))
            add_btn.props("unelevated color=primary")
            add_btn.set_visibility(state.has_permission("payments.create"))

        summary_row = ui.row().classes("w-full gap-4")

        with ui.row().classes("w-full items-end gap-2"):
            direction_options = {"": t("payments.filter.all"), **{d: t(f"status.{d}") for d in DIRECTIONS}}
            status_options = {"": t("payments.filter.all"), **{s: t(f"status.{s}") for s in STATUSES}}
            category_options = {"": t("payments.filter.all"), **{c: t(f"status.{c}") for c in CATEGORIES}}
            direction_f = ui.select(direction_options, value="", label=t("payments.filter.direction")).props(
                "outlined dense"
            ).classes("w-40")
            status_f = ui.select(status_options, value="", label=t("common.status")).props("outlined dense").classes(
                "w-40"
            )
            category_f = ui.select(category_options, value="", label=t("payments.filter.category")).props(
                "outlined dense"
            ).classes("w-40")
            date_from_f = ui.input(t("payments.filter.date_from")).props("outlined dense").classes("w-48")
            date_to_f = ui.input(t("payments.filter.date_to")).props("outlined dense").classes("w-48")
            ui.button(t("payments.filter.apply"), icon="search", on_click=lambda: reload()).props(
                "flat color=primary"
            )

        table = ui.table(columns=columns, rows=[], row_key="id").classes("w-full sp-card").props("flat bordered")
        table.on("rowClick", lambda e: _open_detail_dialog(e.args[1]["id"], reload))
        pagination_row = ui.row().classes("items-center justify-between w-full")

        state_page = {"page": 1, "limit": 20, "total_pages": 1}

        async def reload() -> None:
            state_page["page"] = 1
            await _load()

        async def _load() -> None:
            params = {
                "page": state_page["page"],
                "limit": state_page["limit"],
                "direction": direction_f.value or None,
                "status": status_f.value or None,
                "category": category_f.value or None,
                "date_from": date_from_f.value or None,
                "date_to": date_to_f.value or None,
            }
            try:
                result = await state.client().list_("payments", params)
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            items = result.get("items", [])
            for it in items:
                it["client_name"] = (it.get("client") or {}).get("full_name", "")
                it["direction"] = t(f"status.{it.get('direction')}") if it.get("direction") else ""
                it["category"] = t(f"status.{it.get('category')}") if it.get("category") else ""
                it["status"] = t(f"status.{it.get('status')}") if it.get("status") else ""
            table.rows = items
            meta = result.get("meta", {})
            state_page["total_pages"] = meta.get("total_pages", 1)
            pagination_row.clear()
            with pagination_row:
                ui.label(f"{t('common.total')}: {meta.get('total', 0)}")
                with ui.row().classes("items-center gap-2"):
                    ui.button(icon="chevron_left", on_click=lambda: _change_page(-1)).props("flat dense")
                    ui.label(f"{state_page['page']} / {state_page['total_pages']}")
                    ui.button(icon="chevron_right", on_click=lambda: _change_page(1)).props("flat dense")

            if state.has_permission("reports.read"):
                try:
                    summary = await state.client().payments_summary(
                        {"date_from": date_from_f.value or None, "date_to": date_to_f.value or None}
                    )
                except ApiError:
                    summary = None
                summary_row.clear()
                if summary:
                    with summary_row:
                        for key, label_key, color in [
                            ("income", "payments.summary.income", "text-positive"),
                            ("expense", "payments.summary.expense", "text-negative"),
                            ("refunded", "payments.summary.refunded", "sp-text-2"),
                            ("profit", "payments.summary.profit", "text-primary"),
                            ("debt", "payments.summary.debt", "text-warning"),
                        ]:
                            with ui.card().classes("q-pa-sm sp-card"):
                                ui.label(f"{summary.get(key, 0):,.0f}").classes(f"text-lg font-bold {color}")
                                ui.label(t(label_key)).classes("text-caption sp-muted")

        async def _change_page(delta: int) -> None:
            new_page = state_page["page"] + delta
            if new_page < 1 or new_page > state_page["total_pages"]:
                return
            state_page["page"] = new_page
            await _load()

        ui.timer(0.05, reload, once=True)


async def _search_clients(query: str) -> dict:
    try:
        result = await state.client().list_("clients", {"page": 1, "limit": 20, "search": query})
    except ApiError:
        return {}
    return {c["id"]: f"{c.get('full_name', '')} ({(c.get('code') or '')})" for c in result.get("items", [])}


def _open_create_dialog(on_saved) -> None:
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:460px;"):
        ui.label(t("payments.create.title")).classes("text-lg font-bold")

        client_search = ui.input(t("payments.create.client_search")).props("outlined dense clearable").classes(
            "w-full"
        )
        client_select = ui.select({}, label=t("payments.create.client")).props("outlined dense").classes("w-full")

        async def do_client_search() -> None:
            options = await _search_clients(client_search.value or "")
            client_select.set_options(options)

        client_search.on("keydown.enter", do_client_search)
        ui.button(t("payments.create.client_search_btn"), on_click=do_client_search).props(
            "flat dense color=primary"
        )

        amount = ui.number(t("payments.create.amount"), min=0).props("outlined dense").classes("w-full")
        currency = ui.input(t("payments.create.currency"), value="UZS").props("outlined dense").classes("w-full")
        direction = ui.select(
            {d: t(f"status.{d}") for d in DIRECTIONS}, value="INCOME", label=t("payments.create.direction")
        ).props("outlined dense").classes("w-full")
        category = ui.select(
            {c: t(f"status.{c}") for c in CATEGORIES}, value="SERVICES", label=t("payments.create.category")
        ).props("outlined dense").classes("w-full")
        method = ui.select(
            {"": t("payments.filter.all"), **{m: t(f"status.{m}") for m in METHODS}},
            value="",
            label=t("payments.create.method"),
        ).props("outlined dense").classes("w-full")
        case_id = ui.input(t("payments.create.case_id")).props("outlined dense").classes("w-full")
        contract_id = ui.input(t("payments.create.contract_id")).props("outlined dense").classes("w-full")
        invoice_id = ui.input(t("payments.create.invoice_id")).props("outlined dense").classes("w-full")
        comment = ui.textarea(t("payments.create.comment")).props("outlined dense").classes("w-full")
        err = ui.label("").classes("text-negative text-caption")

        async def save() -> None:
            if not client_select.value:
                err.text = t("payments.err.select_client")
                return
            if not amount.value:
                err.text = t("payments.err.amount_required")
                return
            payload = {
                "client_id": client_select.value,
                "amount": amount.value,
                "currency": currency.value or "UZS",
                "direction": direction.value,
                "category": category.value,
                "method": method.value or None,
                "case_id": case_id.value or None,
                "contract_id": contract_id.value or None,
                "invoice_id": invoice_id.value or None,
                "comment": comment.value or None,
            }
            try:
                await state.client().create("payments", payload)
            except ApiError as exc:
                err.text = exc.message
                return
            ui.notify(t("payments.created"), type="positive")
            dialog.close()
            await on_saved()

        with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
            ui.button(t("common.cancel"), on_click=dialog.close).props("flat")
            ui.button(t("common.save"), on_click=save).props("unelevated color=primary")
    dialog.open()


def _open_detail_dialog(payment_id: str, on_changed) -> None:
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:520px; max-width:680px;"):
        content = ui.column().classes("w-full gap-2")
        with content:
            ui.spinner()

        async def load() -> None:
            try:
                data = await state.client().get("payments", payment_id)
            except ApiError as exc:
                content.clear()
                with content:
                    ui.label(exc.message).classes("text-negative")
                return
            content.clear()
            with content:
                client = data.get("client") or {}
                with ui.row().classes("items-center justify-between w-full"):
                    ui.label(f"{data.get('amount')} {data.get('currency')}").classes("text-xl font-bold")
                    ui.badge(t(f"status.{data.get('status')}") if data.get("status") else "").props(
                        f"color={STATUS_COLORS.get(data.get('status'), 'grey')}"
                    )
                ui.label(f"{t('payments.detail.client')}: {client.get('full_name', '—')}")
                direction_label = t(f"status.{data.get('direction')}") if data.get("direction") else "—"
                category_label = t(f"status.{data.get('category')}") if data.get("category") else "—"
                ui.label(
                    f"{t('payments.detail.type')}: {direction_label} · "
                    f"{t('payments.detail.category')}: {category_label}"
                )
                method_label = t(f"status.{data.get('method')}") if data.get("method") else "—"
                ui.label(f"{t('payments.detail.method')}: {method_label}")
                case = data.get("case") or {}
                contract = data.get("contract") or {}
                if case:
                    ui.label(f"{t('payments.detail.case')}: {case.get('number', '')} — {case.get('title', '')}")
                if contract:
                    ui.label(f"{t('payments.detail.contract')}: № {contract.get('number', '')}")
                ui.label(f"{t('payments.detail.comment')}: {data.get('comment') or '—'}")
                ui.label(f"{t('payments.detail.paid_at')}: {data.get('paid_at') or '—'}").classes(
                    "text-caption sp-muted"
                )

                if state.has_permission("payments.update"):
                    ui.separator().classes("q-my-sm")
                    status_select = ui.select(
                        {s: t(f"status.{s}") for s in STATUSES},
                        value=data.get("status"),
                        label=t("payments.detail.change_status"),
                    ).props("outlined dense").classes("w-full")

                    async def change_status() -> None:
                        try:
                            await state.client().update_payment_status(payment_id, status_select.value)
                        except ApiError as exc:
                            ui.notify(exc.message, type="negative")
                            return
                        ui.notify(t("payments.status_updated"), type="positive")
                        await load()

                    with ui.row().classes("gap-2"):
                        ui.button(t("payments.detail.save_status"), on_click=change_status).props(
                            "flat color=primary"
                        )
                        if data.get("status") == "PAID":
                            async def do_refund() -> None:
                                try:
                                    await state.client().refund_payment(payment_id)
                                except ApiError as exc:
                                    ui.notify(exc.message, type="negative")
                                    return
                                ui.notify(t("payments.refunded_msg"), type="positive")
                                await load()
                                await on_changed()

                            ui.button(t("payments.detail.refund"), on_click=do_refund).props("flat color=negative")

                with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
                    ui.button(t("common.close"), on_click=dialog.close).props("flat")

        ui.timer(0.05, load, once=True)
    dialog.open()
