from __future__ import annotations

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

SERVICE_CATEGORIES = [
    "LEGAL", "ADVOCACY", "CRIMINAL", "ADMINISTRATIVE", "CIVIL",
    "ECONOMIC", "INVESTIGATIVE", "REQUEST", "APPEAL",
]

register(
    {
        "uz": {
            "services.search": "Qidirish (nomi, kodi)",
            "services.category": "Kategoriya",
            "services.all": "Barchasi",
            "services.code": "Kod",
            "services.price": "Narxi",
            "services.active": "Faol",
            "services.inactive": "Nofaol",
            "services.new": "Yangi xizmat",
            "services.edit_title": "Xizmatni tahrirlash",
            "services.new_title": "Yangi xizmat",
            "services.description": "Tavsif",
            "services.sort_order": "Tartib raqami",
            "services.is_active": "Faol",
            "services.name_required": "Nomi va kod majburiy",
            "services.saved": "Saqlandi",
            "services.deleted": "Xizmat o'chirildi",
            "services.total": "Jami: {n} ta",
            "services.see_all": "Barchasi",
        },
        "ru": {
            "services.search": "Поиск (название, код)",
            "services.category": "Категория",
            "services.all": "Все",
            "services.code": "Код",
            "services.price": "Цена",
            "services.active": "Активна",
            "services.inactive": "Неактивна",
            "services.new": "Новая услуга",
            "services.edit_title": "Редактировать услугу",
            "services.new_title": "Новая услуга",
            "services.description": "Описание",
            "services.sort_order": "Порядковый номер",
            "services.is_active": "Активна",
            "services.name_required": "Название и код обязательны",
            "services.saved": "Сохранено",
            "services.deleted": "Услуга удалена",
            "services.total": "Всего: {n}",
            "services.see_all": "Все",
        },
        "en": {
            "services.search": "Search (name, code)",
            "services.category": "Category",
            "services.all": "All",
            "services.code": "Code",
            "services.price": "Price",
            "services.active": "Active",
            "services.inactive": "Inactive",
            "services.new": "New service",
            "services.edit_title": "Edit service",
            "services.new_title": "New service",
            "services.description": "Description",
            "services.sort_order": "Sort order",
            "services.is_active": "Active",
            "services.name_required": "Name and code are required",
            "services.saved": "Saved",
            "services.deleted": "Service deleted",
            "services.total": "Total: {n}",
            "services.see_all": "See all",
        },
    }
)


def render() -> None:
    if not require_login():
        return

    columns = [
        {"name": "code", "label": t("services.code"), "field": "code", "align": "left"},
        {"name": "name", "label": t("common.name"), "field": "name", "align": "left"},
        {"name": "category", "label": t("services.category"), "field": "category", "align": "left"},
        {"name": "base_price", "label": t("services.price"), "field": "base_price", "align": "right"},
        {"name": "is_active_label", "label": t("common.status"), "field": "is_active_label", "align": "left"},
    ]

    with shell(active="/services"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label(t("nav.services")).classes("text-2xl font-bold")
            can_manage = state.has_permission("services.manage")
            add_btn = ui.button(t("services.new"), icon="add", on_click=lambda: _open_form_dialog(None, reload))
            add_btn.props("unelevated color=primary")
            add_btn.set_visibility(can_manage)

        if state.is_client() and state.has_permission("appointments.manage"):
            _specialists_box()

        with ui.row().classes("w-full items-end gap-2"):
            search = ui.input(t("services.search")).props("outlined dense clearable").classes("col")
            category_filter = ui.select(
                [t("services.all")] + SERVICE_CATEGORIES, value=t("services.all"), label=t("services.category")
            ).props("outlined dense").classes("col")

        table = ui.table(columns=columns, rows=[], row_key="id").classes("w-full sp-card").props("flat bordered")
        table.on("rowClick", lambda e: _open_form_dialog(e.args[1], reload))
        pagination_row = ui.row().classes("items-center justify-between w-full")

        state_page = {"page": 1, "limit": 20, "total_pages": 1}

        async def reload() -> None:
            params = {"page": state_page["page"], "limit": state_page["limit"], "search": search.value}
            if category_filter.value and category_filter.value != t("services.all"):
                params["category"] = category_filter.value
            try:
                result = await state.client().list_("services", params)
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            items = result.get("items", [])
            for it in items:
                it["is_active_label"] = t("services.active") if it.get("is_active") else t("services.inactive")
            table.rows = items
            meta = result.get("meta", {})
            state_page["total_pages"] = meta.get("total_pages", 1)
            pagination_row.clear()
            with pagination_row:
                ui.label(t("services.total").format(n=meta.get("total", 0)))
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

        async def _reload_first_page() -> None:
            state_page["page"] = 1
            await reload()

        search.on("keydown.enter", _reload_first_page)
        category_filter.on_value_change(_reload_first_page)
        ui.timer(0.05, reload, once=True)


def _specialists_box() -> None:
    """Mijoz uchun: xizmatlar ro'yxati ustida "Advokat va yuristlar" bloki."""
    from app.pages.specialists import render_specialist_cards

    with ui.column().classes("sp-lane w-full q-pa-md gap-2"):
        with ui.row().classes("w-full items-center justify-between no-wrap"):
            with ui.row().classes("items-center gap-2 no-wrap"):
                ui.icon("balance").classes("text-2xl text-primary")
                ui.label(t("nav.specialists")).classes("text-lg font-bold")
            ui.button(t("services.see_all"), icon="arrow_forward", on_click=lambda: ui.navigate.to("/specialists")).props(
                "flat dense color=primary"
            )
        box = ui.column().classes("w-full")

    async def load() -> None:
        try:
            items = await state.client().list_specialists()
        except ApiError:
            items = []
        box.clear()
        with box:
            render_specialist_cards((items or [])[:6])

    ui.timer(0.05, load, once=True)


def _open_form_dialog(service: dict | None, on_saved) -> None:
    is_edit = service is not None
    can_manage = state.has_permission("services.manage")
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:420px;"):
        ui.label(t("services.edit_title") if is_edit else t("services.new_title")).classes("text-lg font-bold")
        readonly = " disable" if not can_manage else ""
        code = ui.input(f"{t('services.code')} *", value=(service or {}).get("code", "")).props("outlined dense").classes("w-full")
        if is_edit:
            code.props("disable")
        name = ui.input(f"{t('common.name')} *", value=(service or {}).get("name", "")).props(f"outlined dense{readonly}").classes("w-full")
        description = ui.textarea(t("services.description"), value=(service or {}).get("description") or "").props(
            f"outlined dense{readonly}"
        ).classes("w-full")
        category = ui.select(
            SERVICE_CATEGORIES, value=(service or {}).get("category", "LEGAL"), label=t("services.category")
        ).props(f"outlined dense{readonly}").classes("w-full")
        base_price = ui.number(t("services.price"), value=(service or {}).get("base_price")).props(
            f"outlined dense{readonly}"
        ).classes("w-full")
        sort_order = ui.number(t("services.sort_order"), value=(service or {}).get("sort_order", 0)).props(
            f"outlined dense{readonly}"
        ).classes("w-full")
        is_active = ui.checkbox(t("services.is_active"), value=(service or {}).get("is_active", True) if is_edit else True)
        is_active.set_enabled(can_manage)
        err = ui.label("").classes("text-negative text-caption")

        async def save() -> None:
            if not name.value or (not is_edit and not code.value):
                err.text = t("services.name_required")
                return
            if is_edit:
                payload = {
                    "name": name.value,
                    "description": description.value or None,
                    "category": category.value,
                    "base_price": base_price.value,
                    "sort_order": int(sort_order.value) if sort_order.value is not None else 0,
                    "is_active": is_active.value,
                }
            else:
                payload = {
                    "code": code.value,
                    "name": name.value,
                    "description": description.value or None,
                    "category": category.value,
                    "base_price": base_price.value,
                    "sort_order": int(sort_order.value) if sort_order.value is not None else 0,
                }
            try:
                if is_edit:
                    await state.client().update("services", service["id"], payload)
                else:
                    await state.client().create("services", payload)
            except ApiError as exc:
                err.text = exc.message
                return
            ui.notify(t("services.saved"), type="positive")
            dialog.close()
            await on_saved()

        async def remove() -> None:
            try:
                await state.client().delete("services", service["id"])
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            ui.notify(t("services.deleted"), type="positive")
            dialog.close()
            await on_saved()

        with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
            if is_edit and can_manage:
                ui.button(t("common.delete"), on_click=remove).props("flat color=negative")
            ui.button(t("common.cancel") if can_manage else t("common.close"), on_click=dialog.close).props("flat")
            if can_manage:
                ui.button(t("common.save"), on_click=save).props("unelevated color=primary")
    dialog.open()
