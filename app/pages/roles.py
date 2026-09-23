from __future__ import annotations

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

register(
    {
        "uz": {
            "roles.no_access": "Ushbu bo'limni ko'rish uchun ruxsatingiz yo'q",
            "roles.permissions_label": "ruxsat",
            "roles.users_label": "foydalanuvchi",
            "roles.no_permissions": "Ruxsatlar yo'q",
            "roles.new": "Yangi rol",
            "roles.edit": "Tahrirlash",
            "roles.delete": "O'chirish",
            "roles.system_badge": "tizim roli",
            "roles.key_label": "Kalit (masalan PARALEGAL) *",
            "roles.key_hint": "Faqat lotin harf/raqam/pastki chiziq, keyin o'zgartirib bo'lmaydi",
            "roles.name_label": "Nomi *",
            "roles.description_label": "Tavsif",
            "roles.permissions_title": "Ruxsatlar",
            "roles.created": "Rol yaratildi",
            "roles.updated": "Rol yangilandi",
            "roles.deleted": "Rol o'chirildi",
            "roles.confirm_delete": "«{name}» rolini o'chirmoqchimisiz?",
            "roles.key_required": "Kalit va nomi majburiy",
            "roles.system_no_delete": "Tizim rolini o'chirib bo'lmaydi",
            "roles.users_title": "Ushbu rolga biriktirilgan foydalanuvchilar",
            "roles.no_users": "Hech kim biriktirilmagan",
        },
        "ru": {
            "roles.no_access": "У вас нет прав для просмотра этого раздела",
            "roles.permissions_label": "прав",
            "roles.users_label": "пользователей",
            "roles.no_permissions": "Нет прав",
            "roles.new": "Новая роль",
            "roles.edit": "Редактировать",
            "roles.delete": "Удалить",
            "roles.system_badge": "системная роль",
            "roles.key_label": "Ключ (напр. PARALEGAL) *",
            "roles.key_hint": "Только латинские буквы/цифры/подчёркивание, потом не изменить",
            "roles.name_label": "Название *",
            "roles.description_label": "Описание",
            "roles.permissions_title": "Права",
            "roles.created": "Роль создана",
            "roles.updated": "Роль обновлена",
            "roles.deleted": "Роль удалена",
            "roles.confirm_delete": "Удалить роль «{name}»?",
            "roles.key_required": "Ключ и название обязательны",
            "roles.system_no_delete": "Системную роль нельзя удалить",
            "roles.users_title": "Пользователи с этой ролью",
            "roles.no_users": "Никто не назначен",
        },
        "en": {
            "roles.no_access": "You do not have permission to view this section",
            "roles.permissions_label": "permissions",
            "roles.users_label": "users",
            "roles.no_permissions": "No permissions",
            "roles.new": "New role",
            "roles.edit": "Edit",
            "roles.delete": "Delete",
            "roles.system_badge": "system role",
            "roles.key_label": "Key (e.g. PARALEGAL) *",
            "roles.key_hint": "Latin letters/digits/underscore only, cannot be changed later",
            "roles.name_label": "Name *",
            "roles.description_label": "Description",
            "roles.permissions_title": "Permissions",
            "roles.created": "Role created",
            "roles.updated": "Role updated",
            "roles.deleted": "Role deleted",
            "roles.confirm_delete": "Delete role «{name}»?",
            "roles.key_required": "Key and name are required",
            "roles.system_no_delete": "A system role cannot be deleted",
            "roles.users_title": "Users assigned to this role",
            "roles.no_users": "No one assigned",
        },
    }
)


def render() -> None:
    if not require_login():
        return

    with shell(active="/roles"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label(t("nav.roles")).classes("text-2xl font-bold")

            if not state.has_permission("roles.manage"):
                ui.label(t("roles.no_access")).classes("text-red-6")
                return

            ui.button(t("roles.new"), icon="add", on_click=lambda: _open_role_dialog(None, reload)).props(
                "unelevated color=indigo-7"
            )

        container = ui.column().classes("w-full gap-2")

        async def reload() -> None:
            try:
                roles = await state.client().list_("roles")
            except ApiError as exc:
                container.clear()
                with container:
                    ui.label(exc.message).classes("text-red-6")
                return
            container.clear()
            with container:
                for r in roles:
                    _role_card(r, reload)

        ui.timer(0.05, reload, once=True)


def _role_card(r: dict, on_changed) -> None:
    counts = r.get("count", {})
    title = (
        f"{r.get('name')} ({r.get('key')}) — {counts.get('permissions', 0)} "
        f"{t('roles.permissions_label')}, {counts.get('users', 0)} {t('roles.users_label')}"
    )
    with ui.expansion(title).classes("w-full sp-card").props("expand-separator"):
        if r.get("is_system"):
            ui.badge(t("roles.system_badge")).props("color=grey-6")
        if r.get("description"):
            ui.label(r["description"]).classes("text-caption text-grey-6")

        perms = r.get("permissions") or []
        if not perms:
            ui.label(t("roles.no_permissions")).classes("text-caption text-grey-5")
        with ui.row().classes("gap-1 flex-wrap q-mt-xs"):
            for p in perms:
                ui.badge(p.get("key", "")).props("color=indigo-4")

        ui.label(t("roles.users_title")).classes("text-caption text-grey-6 font-medium q-mt-sm")
        users = r.get("users") or []
        if not users:
            ui.label(t("roles.no_users")).classes("text-caption text-grey-5")
        else:
            with ui.row().classes("gap-1 flex-wrap q-mt-xs"):
                for u in users:
                    ui.badge(u.get("email", "")).props("color=grey-7").classes("q-py-xs")

        with ui.row().classes("gap-2 q-mt-sm"):
            ui.button(t("roles.edit"), icon="edit", on_click=lambda r=r: _open_role_dialog(r, on_changed)).props(
                "flat dense color=indigo-7"
            )
            delete_btn = ui.button(
                t("roles.delete"), icon="delete", on_click=lambda r=r: _confirm_delete(r, on_changed)
            ).props("flat dense color=red")
            delete_btn.set_visibility(not r.get("is_system"))


def _confirm_delete(r: dict, on_changed) -> None:
    with ui.dialog() as dialog, ui.card().classes("q-pa-md"):
        ui.label(t("roles.confirm_delete").format(name=r.get("name"))).classes("text-body1")
        with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
            ui.button(t("common.cancel"), on_click=dialog.close).props("flat")

            async def do_delete() -> None:
                try:
                    await state.client().delete("roles", r["id"])
                except ApiError as exc:
                    ui.notify(exc.message, type="negative")
                    return
                ui.notify(t("roles.deleted"), type="positive")
                dialog.close()
                await on_changed()

            ui.button(t("common.delete"), on_click=do_delete).props("unelevated color=red")
    dialog.open()


def _open_role_dialog(role: dict | None, on_changed) -> None:
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:520px;max-width:640px;"):
        ui.label(t("roles.edit") if role else t("roles.new")).classes("text-lg font-bold")

        key_input = ui.input(t("roles.key_label"), value=(role or {}).get("key", "")).props(
            "outlined dense"
        ).classes("w-full")
        if role:
            key_input.props("readonly")
        else:
            ui.label(t("roles.key_hint")).classes("text-caption text-grey-6")
        name_input = ui.input(t("roles.name_label"), value=(role or {}).get("name", "")).props(
            "outlined dense"
        ).classes("w-full")
        description_input = ui.textarea(
            t("roles.description_label"), value=(role or {}).get("description") or ""
        ).props("outlined dense").classes("w-full")

        ui.label(t("roles.permissions_title")).classes("font-medium q-mt-sm")
        checks_col = ui.column().classes("w-full gap-1").style("max-height:280px;overflow-y:auto;")
        checkboxes: dict[str, ui.checkbox] = {}
        selected_ids = {p["id"] for p in (role or {}).get("permissions", [])}

        async def load_permissions() -> None:
            try:
                perms = await state.client().list_("permissions")
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            perms_list = perms if isinstance(perms, list) else perms.get("items", [])
            by_resource: dict[str, list[dict]] = {}
            for p in perms_list:
                by_resource.setdefault(p.get("resource", ""), []).append(p)
            checks_col.clear()
            with checks_col:
                for resource in sorted(by_resource):
                    ui.label(resource).classes("text-caption text-grey-6 font-medium q-mt-xs")
                    with ui.row().classes("gap-3 flex-wrap"):
                        for p in sorted(by_resource[resource], key=lambda x: x.get("key", "")):
                            cb = ui.checkbox(p["key"], value=p["id"] in selected_ids)
                            checkboxes[p["id"]] = cb

        ui.timer(0.05, load_permissions, once=True)

        err = ui.label("").classes("text-red-6 text-caption")

        async def save() -> None:
            permission_ids = [pid for pid, cb in checkboxes.items() if cb.value]
            if role:
                payload = {
                    "name": name_input.value,
                    "description": description_input.value or None,
                    "permission_ids": permission_ids,
                }
                try:
                    await state.client().update("roles", role["id"], payload)
                except ApiError as exc:
                    err.text = exc.message
                    return
                ui.notify(t("roles.updated"), type="positive")
            else:
                if not key_input.value or not name_input.value:
                    err.text = t("roles.key_required")
                    return
                payload = {
                    "key": key_input.value,
                    "name": name_input.value,
                    "description": description_input.value or None,
                    "permission_ids": permission_ids,
                }
                try:
                    await state.client().create("roles", payload)
                except ApiError as exc:
                    err.text = exc.message
                    return
                ui.notify(t("roles.created"), type="positive")
            dialog.close()
            await on_changed()

        with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
            ui.button(t("common.cancel"), on_click=dialog.close).props("flat")
            ui.button(t("common.save"), on_click=save).props("unelevated color=indigo-7")
    dialog.open()
