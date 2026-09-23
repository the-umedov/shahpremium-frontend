from __future__ import annotations

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

register(
    {
        "uz": {
            "notifications.forbidden": "Bu sahifa uchun ruxsatingiz yo'q",
            "notifications.mark_all": "Hammasini o'qilgan deb belgilash",
            "notifications.unread_only": "Faqat o'qilmaganlar",
            "notifications.empty": "Bildirishnomalar yo'q",
            "notifications.marked_all": "Barchasi o'qilgan deb belgilandi",
            "notifications.total_label": "Jami: {n} ta",
        },
        "ru": {
            "notifications.forbidden": "У вас нет доступа к этой странице",
            "notifications.mark_all": "Отметить все как прочитанные",
            "notifications.unread_only": "Только непрочитанные",
            "notifications.empty": "Уведомлений нет",
            "notifications.marked_all": "Все отмечены как прочитанные",
            "notifications.total_label": "Всего: {n}",
        },
        "en": {
            "notifications.forbidden": "You don't have permission to view this page",
            "notifications.mark_all": "Mark all as read",
            "notifications.unread_only": "Unread only",
            "notifications.empty": "No notifications",
            "notifications.marked_all": "All marked as read",
            "notifications.total_label": "Total: {n}",
        },
    }
)


def render() -> None:
    if not require_login():
        return

    with shell(active="/notifications"):
        if not state.has_permission("notifications.read"):
            ui.label(t("notifications.forbidden")).classes("text-negative")
            return

        with ui.row().classes("w-full items-center justify-between"):
            ui.label(t("nav.notifications")).classes("text-2xl font-bold")
            mark_all_btn = ui.button(
                t("notifications.mark_all"), icon="done_all", on_click=lambda: _mark_all(reload)
            )
            mark_all_btn.props("flat color=primary")

        unread_only = ui.switch(t("notifications.unread_only"), on_change=lambda e: reload())

        list_col = ui.column().classes("w-full gap-1")
        pagination_row = ui.row().classes("items-center justify-between w-full")

        state_page = {"page": 1, "limit": 20, "total_pages": 1}

        async def reload() -> None:
            try:
                result = await state.client().list_notifications(
                    {
                        "page": state_page["page"],
                        "limit": state_page["limit"],
                        "unread_only": "true" if unread_only.value else None,
                    }
                )
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            items = result.get("items", [])
            list_col.clear()
            with list_col:
                if not items:
                    ui.label(t("notifications.empty")).classes("text-caption sp-subtle")
                for it in items:
                    _render_item(it)
            meta = result.get("meta", {})
            state_page["total_pages"] = meta.get("total_pages", 1)
            pagination_row.clear()
            with pagination_row:
                ui.label(t("notifications.total_label").format(n=meta.get("total", 0)))
                with ui.row().classes("items-center gap-2"):
                    ui.button(icon="chevron_left", on_click=lambda: _change_page(-1)).props("flat dense")
                    ui.label(f"{state_page['page']} / {state_page['total_pages']}")
                    ui.button(icon="chevron_right", on_click=lambda: _change_page(1)).props("flat dense")

        async def _change_page(delta: int) -> None:
            new_page = state_page["page"] + delta
            if new_page < 1 or new_page > state_page["total_pages"]:
                return
            state_page["page"] = new_page
            await reload()

        def _render_item(it: dict) -> None:
            is_read = bool(it.get("is_read"))
            with ui.row().classes(
                "w-full items-start gap-3 q-pa-sm sp-card cursor-pointer "
                + ("" if is_read else "sp-active")
            ).on("click", lambda i=it: _mark_one(i["id"])):
                ui.icon("fiber_manual_record" if not is_read else "check_circle").classes(
                    ("text-primary" if not is_read else "sp-subtle") + " text-xs q-mt-xs"
                )
                with ui.column().classes("gap-0 col"):
                    ui.label(it.get("title", "")).classes("font-bold" if not is_read else "font-normal")
                    ui.label(it.get("body", "")).classes("text-sm sp-text-2")
                    ui.label(str(it.get("created_at", ""))[:19]).classes("text-caption sp-subtle")

        async def _mark_one(notification_id: str) -> None:
            try:
                await state.client().notifications_read_one(notification_id)
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            await reload()

        async def _mark_all(on_changed) -> None:
            try:
                await state.client().notifications_read_all()
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            ui.notify(t("notifications.marked_all"), type="positive")
            await on_changed()

        ui.timer(0.05, reload, once=True)
