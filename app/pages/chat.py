from __future__ import annotations

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

register(
    {
        "uz": {
            "chat.forbidden": "Bu sahifa uchun ruxsatingiz yo'q",
            "chat.default_label": "Suhbat",
            "chat.list_title": "Suhbatlar ro'yxati",
            "chat.empty": "Suhbatlar yo'q",
            "chat.select_chat": "Suhbatni tanlang",
            "chat.no_messages": "Xabarlar yo'q",
            "chat.message_placeholder": "Xabar yozing...",
            "chat.attachment_label": "Fayl: {name}",
            "chat.new_chat_title": "Yangi suhbat",
            "chat.title_optional": "Sarlavha (ixtiyoriy)",
            "chat.members_label": "A'zolar (foydalanuvchi ID'lari, vergul bilan) *",
            "chat.internal_switch": "Ichki suhbat (faqat xodimlar)",
            "chat.case_id_optional": "Ish ID (ixtiyoriy)",
            "chat.client_id_optional": "Mijoz ID (ixtiyoriy)",
            "chat.member_required": "Kamida bitta a'zo ID kerak",
            "chat.created": "Suhbat yaratildi",
        },
        "ru": {
            "chat.forbidden": "У вас нет доступа к этой странице",
            "chat.default_label": "Чат",
            "chat.list_title": "Список чатов",
            "chat.empty": "Чатов нет",
            "chat.select_chat": "Выберите чат",
            "chat.no_messages": "Сообщений нет",
            "chat.message_placeholder": "Напишите сообщение...",
            "chat.attachment_label": "Файл: {name}",
            "chat.new_chat_title": "Новый чат",
            "chat.title_optional": "Заголовок (необязательно)",
            "chat.members_label": "Участники (ID пользователей, через запятую) *",
            "chat.internal_switch": "Внутренний чат (только сотрудники)",
            "chat.case_id_optional": "ID дела (необязательно)",
            "chat.client_id_optional": "ID клиента (необязательно)",
            "chat.member_required": "Нужен хотя бы один ID участника",
            "chat.created": "Чат создан",
        },
        "en": {
            "chat.forbidden": "You don't have permission to view this page",
            "chat.default_label": "Chat",
            "chat.list_title": "Chat list",
            "chat.empty": "No chats",
            "chat.select_chat": "Select a chat",
            "chat.no_messages": "No messages",
            "chat.message_placeholder": "Type a message...",
            "chat.attachment_label": "File: {name}",
            "chat.new_chat_title": "New chat",
            "chat.title_optional": "Title (optional)",
            "chat.members_label": "Members (user IDs, comma-separated) *",
            "chat.internal_switch": "Internal chat (staff only)",
            "chat.case_id_optional": "Case ID (optional)",
            "chat.client_id_optional": "Client ID (optional)",
            "chat.member_required": "At least one member ID is required",
            "chat.created": "Chat created",
        },
    }
)


def _chat_label(chat: dict | None, my_id: str) -> str:
    if not chat:
        return t("chat.default_label")
    if chat.get("title"):
        return chat["title"]
    names = []
    for m in chat.get("members") or []:
        user = m.get("user") or {}
        if user.get("id") == my_id:
            continue
        profile = user.get("profile") or {}
        name = f"{profile.get('first_name', '')} {profile.get('last_name', '')}".strip()
        names.append(name or (user.get("id") or "")[:8])
    return ", ".join(names) or t("chat.default_label")


def render() -> None:
    if not require_login():
        return

    if not state.has_permission("chat.use"):
        with shell(active="/chat"):
            ui.label(t("chat.forbidden")).classes("text-negative")
        return

    me = state.get_me() or {}
    my_id = me.get("id", "")

    with shell(active="/chat"):
        ui.label(t("nav.chat")).classes("text-2xl font-bold")

        ui_state = {"chats": [], "chat_id": None}

        with ui.row().classes("w-full gap-4 no-wrap").style("height:70vh;"):
            with ui.column().classes("sp-card q-pa-sm").style(
                "width:320px; min-width:280px; height:100%; overflow-y:auto;"
            ):
                with ui.row().classes("w-full items-center justify-between"):
                    ui.label(t("chat.list_title")).classes("font-semibold")
                    ui.button(icon="add", on_click=lambda: _open_new_chat_dialog(reload_chats)).props(
                        "flat dense round color=primary"
                    )
                chat_list_col = ui.column().classes("w-full gap-1")

            with ui.column().classes("sp-card q-pa-sm col").style("height:100%;"):
                header_row = ui.row().classes("w-full items-center justify-between")
                messages_col = ui.column().classes("w-full gap-2").style(
                    "flex:1 1 auto; overflow-y:auto; min-height:0;"
                )
                with ui.row().classes("w-full items-center gap-2 q-mt-sm"):
                    msg_input = ui.input(t("chat.message_placeholder")).props("outlined dense").classes("col")
                    send_btn = ui.button(icon="send")

        async def reload_chats() -> None:
            try:
                chats = await state.client().list_chats()
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            ui_state["chats"] = chats
            chat_list_col.clear()
            with chat_list_col:
                if not chats:
                    ui.label(t("chat.empty")).classes("text-caption sp-subtle")
                for c in chats:
                    is_active = c["id"] == ui_state["chat_id"]
                    with ui.row().classes(
                        "w-full items-center justify-between q-pa-sm rounded-borders cursor-pointer "
                        + ("sp-active" if is_active else "")
                    ).on("click", lambda cid=c["id"]: open_chat(cid)):
                        with ui.column().classes("gap-0"):
                            ui.label(_chat_label(c, my_id)).classes("text-sm font-medium")
                            last = c.get("last_message") or {}
                            ui.label(last.get("body", "")).classes("text-caption sp-muted").style(
                                "max-width:200px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;"
                            )
                        if c.get("unread"):
                            ui.badge(str(c["unread"])).props("color=negative")

        async def open_chat(chat_id: str) -> None:
            ui_state["chat_id"] = chat_id
            await reload_chats()
            await reload_messages()
            try:
                await state.client().chat_mark_read(chat_id)
            except ApiError:
                pass

        async def reload_messages() -> None:
            chat_id = ui_state["chat_id"]
            header_row.clear()
            if not chat_id:
                messages_col.clear()
                with header_row:
                    ui.label(t("chat.select_chat")).classes("sp-muted")
                return
            chat = next((c for c in ui_state["chats"] if c["id"] == chat_id), None)
            with header_row:
                ui.label(_chat_label(chat, my_id)).classes("font-semibold")
            try:
                msgs = await state.client().chat_messages(chat_id)
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            msgs = list(reversed(msgs))  # backend eng yangisini birinchi qaytaradi
            messages_col.clear()
            with messages_col:
                if not msgs:
                    ui.label(t("chat.no_messages")).classes("text-caption sp-subtle")
                for m in msgs:
                    is_mine = m.get("sender_id") == my_id
                    sender = m.get("sender") or {}
                    profile = sender.get("profile") or {}
                    sender_name = f"{profile.get('first_name', '')} {profile.get('last_name', '')}".strip() or "?"
                    with ui.row().classes("w-full " + ("justify-end" if is_mine else "justify-start")):
                        with ui.column().classes(
                            "q-pa-sm rounded-borders "
                            + ("bg-primary text-white" if is_mine else "sp-surface-2")
                        ).style("max-width:70%;"):
                            if not is_mine:
                                ui.label(sender_name).classes("text-caption font-bold")
                            ui.label(m.get("body", ""))
                            if m.get("attachment_name"):
                                ui.label(t("chat.attachment_label").format(name=m["attachment_name"])).classes(
                                    "text-caption"
                                )
                            ui.label(str(m.get("created_at", ""))[:19]).classes("text-caption opacity-70")

        async def send() -> None:
            chat_id = ui_state["chat_id"]
            if not chat_id or not msg_input.value:
                return
            body = msg_input.value
            msg_input.value = ""
            try:
                await state.client().send_chat_message(chat_id, body)
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            await reload_messages()
            await reload_chats()

        send_btn.on_click(send)
        msg_input.on("keydown.enter", send)

        async def poll() -> None:
            if ui_state["chat_id"]:
                await reload_messages()
            await reload_chats()

        ui.timer(3.0, poll)
        ui.timer(0.05, reload_chats, once=True)


def _open_new_chat_dialog(on_saved) -> None:
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:420px;"):
        ui.label(t("chat.new_chat_title")).classes("text-lg font-bold")
        title = ui.input(t("chat.title_optional")).props("outlined dense").classes("w-full")
        member_ids = ui.input(t("chat.members_label")).props(
            "outlined dense"
        ).classes("w-full")
        is_internal = ui.switch(t("chat.internal_switch"))
        case_id = ui.input(t("chat.case_id_optional")).props("outlined dense").classes("w-full")
        client_id = ui.input(t("chat.client_id_optional")).props("outlined dense").classes("w-full")
        err = ui.label("").classes("text-negative text-caption")

        async def save() -> None:
            ids = [x.strip() for x in (member_ids.value or "").split(",") if x.strip()]
            if not ids:
                err.text = t("chat.member_required")
                return
            payload = {
                "member_ids": ids,
                "title": title.value or None,
                "is_internal": is_internal.value,
                "case_id": case_id.value or None,
                "client_id": client_id.value or None,
            }
            try:
                await state.client().create_chat(payload)
            except ApiError as exc:
                err.text = exc.message
                return
            ui.notify(t("chat.created"), type="positive")
            dialog.close()
            await on_saved()

        with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
            ui.button(t("common.cancel"), on_click=dialog.close).props("flat")
            ui.button(t("common.create"), on_click=save).props("unelevated color=primary")
    dialog.open()
