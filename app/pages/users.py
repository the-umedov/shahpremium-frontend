from __future__ import annotations

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

register(
    {
        "uz": {
            "users.search": "Qidirish (email)",
            "users.col.email": "Email",
            "users.col.phone": "Telefon",
            "users.col.type": "Turi",
            "users.col.roles": "Rollar",
            "users.col.active": "Faol",
            "users.detail.fullname": "F.I.Sh.",
            "users.detail.phone": "Telefon",
            "users.detail.type": "Turi",
            "users.detail.region": "Hudud",
            "users.detail.active_switch": "Faol",
            "users.detail.roles_heading": "Rollar",
            "users.detail.roles_select": "Rollarni tanlang",
            "users.updated": "Foydalanuvchi yangilandi",
        },
        "ru": {
            "users.search": "Поиск (email)",
            "users.col.email": "Email",
            "users.col.phone": "Телефон",
            "users.col.type": "Тип",
            "users.col.roles": "Роли",
            "users.col.active": "Активен",
            "users.detail.fullname": "Ф.И.О.",
            "users.detail.phone": "Телефон",
            "users.detail.type": "Тип",
            "users.detail.region": "Регион",
            "users.detail.active_switch": "Активен",
            "users.detail.roles_heading": "Роли",
            "users.detail.roles_select": "Выберите роли",
            "users.updated": "Пользователь обновлён",
        },
        "en": {
            "users.search": "Search (email)",
            "users.col.email": "Email",
            "users.col.phone": "Phone",
            "users.col.type": "Type",
            "users.col.roles": "Roles",
            "users.col.active": "Active",
            "users.detail.fullname": "Full name",
            "users.detail.phone": "Phone",
            "users.detail.type": "Type",
            "users.detail.region": "Region",
            "users.detail.active_switch": "Active",
            "users.detail.roles_heading": "Roles",
            "users.detail.roles_select": "Select roles",
            "users.updated": "User updated",
        },
    }
)


def render() -> None:
    if not require_login():
        return

    columns = [
        {"name": "email", "label": t("users.col.email"), "field": "email", "align": "left"},
        {"name": "phone", "label": t("users.col.phone"), "field": "phone", "align": "left"},
        {"name": "type", "label": t("users.col.type"), "field": "type", "align": "left"},
        {"name": "roles_names", "label": t("users.col.roles"), "field": "roles_names", "align": "left"},
        {"name": "is_active_label", "label": t("users.col.active"), "field": "is_active_label", "align": "left"},
    ]

    with shell(active="/users"):
        ui.label(t("nav.users")).classes("text-2xl font-bold")

        search = ui.input(t("users.search")).props("outlined dense clearable").classes("w-full")
        table = ui.table(columns=columns, rows=[], row_key="id").classes("w-full sp-card").props("flat bordered")
        table.on("rowClick", lambda e: _open_detail_dialog(e.args[1], reload))
        pagination_row = ui.row().classes("items-center justify-between w-full")

        state_page = {"page": 1, "limit": 20, "total_pages": 1}

        async def reload() -> None:
            state_page["page"] = 1
            await _load()

        async def _load() -> None:
            try:
                result = await state.client().list_(
                    "users", {"page": state_page["page"], "limit": state_page["limit"], "search": search.value}
                )
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            items = result.get("items", [])
            for it in items:
                profile = it.get("profile") or {}
                it["full_name"] = f"{profile.get('last_name', '')} {profile.get('first_name', '')}".strip()
                it["roles_names"] = ", ".join(r.get("name", "") for r in (it.get("roles") or []))
                it["is_active_label"] = t("common.yes") if it.get("is_active") else t("common.no")
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

        async def _change_page(delta: int) -> None:
            new_page = state_page["page"] + delta
            if new_page < 1 or new_page > state_page["total_pages"]:
                return
            state_page["page"] = new_page
            await _load()

        search.on("keydown.enter", reload)
        ui.timer(0.05, reload, once=True)


def _open_detail_dialog(user_row: dict, on_changed) -> None:
    user_id = user_row["id"]
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:480px; max-width:640px;"):
        content = ui.column().classes("w-full gap-2")
        with content:
            profile = user_row.get("profile") or {}
            region = user_row.get("region") or {}
            ui.label(user_row.get("email") or user_row.get("phone") or "").classes("text-xl font-bold")
            ui.label(
                f"{t('users.detail.fullname')}: "
                + (f"{profile.get('last_name', '')} {profile.get('first_name', '')}".strip() or "—")
            )
            ui.label(f"{t('users.detail.phone')}: {user_row.get('phone') or '—'}")
            ui.label(f"{t('users.detail.type')}: {user_row.get('type') or '—'}")
            ui.label(f"{t('users.detail.region')}: {region.get('name') or '—'}")

            can_update = state.has_permission("users.update")
            active_switch = ui.switch(t("users.detail.active_switch"), value=bool(user_row.get("is_active")))
            active_switch.set_enabled(can_update)

            ui.separator().classes("q-my-sm")
            ui.label(t("users.detail.roles_heading")).classes("text-md font-semibold")
            roles_select = ui.select({}, label=t("users.detail.roles_select"), multiple=True).props(
                "outlined dense use-chips"
            ).classes("w-full")
            roles_select.set_enabled(can_update)
            err = ui.label("").classes("text-negative text-caption")

            async def load_roles() -> None:
                try:
                    all_roles = await state.client().list_("roles")
                except ApiError as exc:
                    err.text = exc.message
                    return
                options = {r["id"]: r["name"] for r in all_roles}
                roles_select.set_options(options)
                current_keys = {r.get("key") for r in (user_row.get("roles") or [])}
                current_ids = [r["id"] for r in all_roles if r.get("key") in current_keys]
                roles_select.value = current_ids

            ui.timer(0.05, load_roles, once=True)

            if can_update:
                async def save() -> None:
                    try:
                        await state.client().update("users", user_id, {"is_active": active_switch.value})
                        await state.client().set_user_roles(user_id, roles_select.value or [])
                    except ApiError as exc:
                        err.text = exc.message
                        return
                    ui.notify(t("users.updated"), type="positive")
                    dialog.close()
                    await on_changed()

                with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
                    ui.button(t("common.cancel"), on_click=dialog.close).props("flat")
                    ui.button(t("common.save"), on_click=save).props("unelevated color=primary")
            else:
                with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
                    ui.button(t("common.close"), on_click=dialog.close).props("flat")
    dialog.open()
