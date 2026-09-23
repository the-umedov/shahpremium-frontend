from __future__ import annotations

import json

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

register(
    {
        "uz": {
            "audit.forbidden": "Bu sahifa uchun ruxsatingiz yo'q",
            "audit.col_time": "Vaqt",
            "audit.col_actor": "Foydalanuvchi",
            "audit.col_entity": "Obyekt",
            "audit.col_entity_id": "Obyekt ID",
            "audit.col_action": "Amal",
            "audit.filter_actor": "Foydalanuvchi ID",
            "audit.filter_entity": "Obyekt turi (masalan: clients)",
            "audit.filter_action": "Amal (masalan: create)",
            "audit.filter_date_from": "Sanadan",
            "audit.filter_date_to": "Sanagacha",
            "audit.filter_btn": "Filtrlash",
            "audit.total_label": "Jami: {n} ta",
            "audit.detail_time": "Vaqt: {value}",
            "audit.detail_actor": "Foydalanuvchi ID: {value}",
            "audit.detail_entity_id": "Obyekt ID: {value}",
            "audit.detail_reason": "Sabab: {value}",
            "audit.before": "Oldin (before)",
            "audit.after": "Keyin (after)",
        },
        "ru": {
            "audit.forbidden": "У вас нет доступа к этой странице",
            "audit.col_time": "Время",
            "audit.col_actor": "Пользователь",
            "audit.col_entity": "Объект",
            "audit.col_entity_id": "ID объекта",
            "audit.col_action": "Действие",
            "audit.filter_actor": "ID пользователя",
            "audit.filter_entity": "Тип объекта (например: clients)",
            "audit.filter_action": "Действие (например: create)",
            "audit.filter_date_from": "С даты",
            "audit.filter_date_to": "По дату",
            "audit.filter_btn": "Фильтровать",
            "audit.total_label": "Всего: {n}",
            "audit.detail_time": "Время: {value}",
            "audit.detail_actor": "ID пользователя: {value}",
            "audit.detail_entity_id": "ID объекта: {value}",
            "audit.detail_reason": "Причина: {value}",
            "audit.before": "До (before)",
            "audit.after": "После (after)",
        },
        "en": {
            "audit.forbidden": "You don't have permission to view this page",
            "audit.col_time": "Time",
            "audit.col_actor": "User",
            "audit.col_entity": "Entity",
            "audit.col_entity_id": "Entity ID",
            "audit.col_action": "Action",
            "audit.filter_actor": "User ID",
            "audit.filter_entity": "Entity type (e.g. clients)",
            "audit.filter_action": "Action (e.g. create)",
            "audit.filter_date_from": "From date",
            "audit.filter_date_to": "To date",
            "audit.filter_btn": "Filter",
            "audit.total_label": "Total: {n}",
            "audit.detail_time": "Time: {value}",
            "audit.detail_actor": "User ID: {value}",
            "audit.detail_entity_id": "Entity ID: {value}",
            "audit.detail_reason": "Reason: {value}",
            "audit.before": "Before",
            "audit.after": "After",
        },
    }
)


def render() -> None:
    if not require_login():
        return

    with shell(active="/audit"):
        if not state.has_permission("audit.read"):
            ui.label(t("audit.forbidden")).classes("text-negative")
            return

        ui.label(t("nav.audit")).classes("text-2xl font-bold")

        columns = [
            {"name": "created_at", "label": t("audit.col_time"), "field": "created_at", "align": "left"},
            {"name": "actor_id", "label": t("audit.col_actor"), "field": "actor_id", "align": "left"},
            {"name": "entity", "label": t("audit.col_entity"), "field": "entity", "align": "left"},
            {"name": "entity_id", "label": t("audit.col_entity_id"), "field": "entity_id", "align": "left"},
            {"name": "action", "label": t("audit.col_action"), "field": "action", "align": "left"},
        ]

        with ui.row().classes("w-full items-end gap-2 flex-wrap"):
            actor_id = ui.input(t("audit.filter_actor")).props("outlined dense clearable").classes("col-2")
            entity = ui.input(t("audit.filter_entity")).props("outlined dense clearable").classes("col-2")
            action = ui.input(t("audit.filter_action")).props("outlined dense clearable").classes("col-2")
            date_from = ui.input(t("audit.filter_date_from")).props("outlined dense type=date").classes("col-2")
            date_to = ui.input(t("audit.filter_date_to")).props("outlined dense type=date").classes("col-2")
            filter_btn = ui.button(t("audit.filter_btn"), icon="search", on_click=lambda: reload())
            filter_btn.props("unelevated color=primary")

        table = ui.table(columns=columns, rows=[], row_key="id").classes("w-full sp-card").props("flat bordered")
        table.on("rowClick", lambda e: _open_detail_dialog(e.args[1]))
        pagination_row = ui.row().classes("items-center justify-between w-full")

        state_page = {"page": 1, "limit": 30, "total_pages": 1}

        async def reload() -> None:
            state_page["page"] = 1
            await _load_page()

        async def _load_page() -> None:
            try:
                result = await state.client().list_audit_logs(
                    {
                        "page": state_page["page"],
                        "limit": state_page["limit"],
                        "actor_id": actor_id.value or None,
                        "entity": entity.value or None,
                        "action": action.value or None,
                        "date_from": date_from.value or None,
                        "date_to": date_to.value or None,
                    }
                )
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            items = result.get("items", [])
            display_rows = []
            for it in items:
                row = dict(it)
                row["actor_id"] = (it.get("actor_id") or "—")[:8] if it.get("actor_id") else "—"
                row["created_at"] = str(it.get("created_at", ""))[:19]
                row["_raw"] = it
                display_rows.append(row)
            table.rows = display_rows
            meta = result.get("meta", {})
            state_page["total_pages"] = meta.get("total_pages", 1)
            pagination_row.clear()
            with pagination_row:
                ui.label(t("audit.total_label").format(n=meta.get("total", 0)))
                with ui.row().classes("items-center gap-2"):
                    ui.button(icon="chevron_left", on_click=lambda: _change_page(-1)).props("flat dense")
                    ui.label(f"{state_page['page']} / {state_page['total_pages']}")
                    ui.button(icon="chevron_right", on_click=lambda: _change_page(1)).props("flat dense")

        async def _change_page(delta: int) -> None:
            new_page = state_page["page"] + delta
            if new_page < 1 or new_page > state_page["total_pages"]:
                return
            state_page["page"] = new_page
            await _load_page()

        ui.timer(0.05, reload, once=True)


def _open_detail_dialog(row: dict) -> None:
    raw = row.get("_raw", row)
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:520px; max-width:760px;"):
        ui.label(f"{raw.get('entity', '')} — {raw.get('action', '')}").classes("text-lg font-bold")
        ui.label(t("audit.detail_time").format(value=raw.get("created_at", ""))).classes(
            "text-caption sp-muted"
        )
        ui.label(t("audit.detail_actor").format(value=raw.get("actor_id") or "—"))
        ui.label(t("audit.detail_entity_id").format(value=raw.get("entity_id") or "—"))
        if raw.get("reason"):
            ui.label(t("audit.detail_reason").format(value=raw["reason"]))
        ui.separator().classes("q-my-sm")
        with ui.row().classes("w-full gap-4"):
            with ui.column().classes("col"):
                ui.label(t("audit.before")).classes("font-semibold")
                ui.code(
                    json.dumps(raw.get("before"), ensure_ascii=False, indent=2) if raw.get("before") else "—"
                ).classes("w-full")
            with ui.column().classes("col"):
                ui.label(t("audit.after")).classes("font-semibold")
                ui.code(
                    json.dumps(raw.get("after"), ensure_ascii=False, indent=2) if raw.get("after") else "—"
                ).classes("w-full")
        with ui.row().classes("w-full justify-end q-mt-md"):
            ui.button(t("common.close"), on_click=dialog.close).props("flat")
    dialog.open()
