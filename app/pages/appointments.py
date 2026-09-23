from __future__ import annotations

import json
from datetime import datetime, timedelta

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

APPOINTMENT_STATUSES = [
    "PENDING", "SCHEDULED", "CONFIRMED", "IN_PROGRESS", "COMPLETED", "CANCELLED", "NO_SHOW",
]
SPECIALIST_KIND_KEYS = [None, "LAWYER", "ADVOCATE", "STAFF"]
QUEUE_STATUS_KEYS = ["WAITING", "INVITED", "IN_SERVICE", "DONE", "CANCELLED"]
QUEUE_FLOW = {"WAITING": "INVITED", "INVITED": "IN_SERVICE", "IN_SERVICE": "DONE"}

register(
    {
        "uz": {
            "appointments.book": "Band qilish",
            "appointments.tab_list": "Ro'yxat",
            "appointments.tab_queue": "Navbat",
            "appointments.col_title": "Sarlavha",
            "appointments.col_start": "Boshlanishi",
            "appointments.col_end": "Tugashi",
            "appointments.col_location": "Manzil",
            "appointments.total_period": "oxirgi 7 kun — keyingi 30 kun",
            "appointments.refresh": "Yangilash",
            "appointments.join_assignee_placeholder": "Mutaxassis ID (ixtiyoriy)",
            "appointments.join_client_placeholder": "Mijoz ID (ixtiyoriy)",
            "appointments.join_queue_btn": "Navbatga yozish",
            "appointments.joined_queue_notify": "Navbatga qo'shildi",
            "appointments.queue_empty": "Bo'sh",
            "appointments.book_dialog_title": "Yangi uchrashuv band qilish",
            "appointments.specialist_kind_label": "Mutaxassis turi",
            "appointments.kind_all": "Hammasi",
            "appointments.kind_lawyer": "Yurist",
            "appointments.kind_advocate": "Advokat",
            "appointments.kind_staff": "Xodim",
            "appointments.search_by_name": "Qidirish (ism)",
            "appointments.specialist_label": "Mutaxassis *",
            "appointments.search_specialists_btn": "Mutaxassislarni qidirish",
            "appointments.date_label": "Sana *",
            "appointments.no_time_selected": "Vaqt tanlanmagan",
            "appointments.selected_time_prefix": "Tanlangan vaqt",
            "appointments.select_specialist_and_date_first": "Avval mutaxassis va sanani tanlang",
            "appointments.no_slots": "Bu kunda bo'sh vaqt yo'q",
            "appointments.view_availability_btn": "Bo'sh vaqtlarni ko'rish",
            "appointments.title_field": "Sarlavha *",
            "appointments.client_id_field": "Mijoz ID",
            "appointments.case_id_field": "Ish ID",
            "appointments.required_fields_err": "Mutaxassis, vaqt va sarlavha majburiy",
            "appointments.booked_notify": "Uchrashuv band qilindi",
            "appointments.change_status_label": "Holatni o'zgartirish",
            "appointments.save_status_btn": "Holatni saqlash",
            "appointments.status_updated_notify": "Holat yangilandi",
        },
        "ru": {
            "appointments.book": "Забронировать",
            "appointments.tab_list": "Список",
            "appointments.tab_queue": "Очередь",
            "appointments.col_title": "Заголовок",
            "appointments.col_start": "Начало",
            "appointments.col_end": "Окончание",
            "appointments.col_location": "Адрес",
            "appointments.total_period": "последние 7 дней — следующие 30 дней",
            "appointments.refresh": "Обновить",
            "appointments.join_assignee_placeholder": "ID специалиста (необязательно)",
            "appointments.join_client_placeholder": "ID клиента (необязательно)",
            "appointments.join_queue_btn": "Встать в очередь",
            "appointments.joined_queue_notify": "Добавлено в очередь",
            "appointments.queue_empty": "Пусто",
            "appointments.book_dialog_title": "Новая запись",
            "appointments.specialist_kind_label": "Тип специалиста",
            "appointments.kind_all": "Все",
            "appointments.kind_lawyer": "Юрист",
            "appointments.kind_advocate": "Адвокат",
            "appointments.kind_staff": "Сотрудник",
            "appointments.search_by_name": "Поиск (имя)",
            "appointments.specialist_label": "Специалист *",
            "appointments.search_specialists_btn": "Найти специалистов",
            "appointments.date_label": "Дата *",
            "appointments.no_time_selected": "Время не выбрано",
            "appointments.selected_time_prefix": "Выбранное время",
            "appointments.select_specialist_and_date_first": "Сначала выберите специалиста и дату",
            "appointments.no_slots": "На этот день нет свободного времени",
            "appointments.view_availability_btn": "Показать свободное время",
            "appointments.title_field": "Заголовок *",
            "appointments.client_id_field": "ID клиента",
            "appointments.case_id_field": "ID дела",
            "appointments.required_fields_err": "Специалист, время и заголовок обязательны",
            "appointments.booked_notify": "Запись создана",
            "appointments.change_status_label": "Изменить статус",
            "appointments.save_status_btn": "Сохранить статус",
            "appointments.status_updated_notify": "Статус обновлён",
        },
        "en": {
            "appointments.book": "Book",
            "appointments.tab_list": "List",
            "appointments.tab_queue": "Queue",
            "appointments.col_title": "Title",
            "appointments.col_start": "Start",
            "appointments.col_end": "End",
            "appointments.col_location": "Location",
            "appointments.total_period": "last 7 days — next 30 days",
            "appointments.refresh": "Refresh",
            "appointments.join_assignee_placeholder": "Specialist ID (optional)",
            "appointments.join_client_placeholder": "Client ID (optional)",
            "appointments.join_queue_btn": "Join queue",
            "appointments.joined_queue_notify": "Added to the queue",
            "appointments.queue_empty": "Empty",
            "appointments.book_dialog_title": "New appointment",
            "appointments.specialist_kind_label": "Specialist type",
            "appointments.kind_all": "All",
            "appointments.kind_lawyer": "Lawyer",
            "appointments.kind_advocate": "Advocate",
            "appointments.kind_staff": "Staff",
            "appointments.search_by_name": "Search (name)",
            "appointments.specialist_label": "Specialist *",
            "appointments.search_specialists_btn": "Search specialists",
            "appointments.date_label": "Date *",
            "appointments.no_time_selected": "No time selected",
            "appointments.selected_time_prefix": "Selected time",
            "appointments.select_specialist_and_date_first": "Select a specialist and date first",
            "appointments.no_slots": "No free time on this day",
            "appointments.view_availability_btn": "View availability",
            "appointments.title_field": "Title *",
            "appointments.client_id_field": "Client ID",
            "appointments.case_id_field": "Case ID",
            "appointments.required_fields_err": "Specialist, time, and title are required",
            "appointments.booked_notify": "Appointment booked",
            "appointments.change_status_label": "Change status",
            "appointments.save_status_btn": "Save status",
            "appointments.status_updated_notify": "Status updated",
        },
    }
)

# Enum display strings shared across modules under the `status.*` namespace.
register(
    {
        "uz": {
            "status.PENDING": "Kutilmoqda",
            "status.SCHEDULED": "Rejalashtirilgan",
            "status.CONFIRMED": "Tasdiqlangan",
            "status.IN_PROGRESS": "Jarayonda",
            "status.COMPLETED": "Yakunlangan",
            "status.CANCELLED": "Bekor qilindi",
            "status.NO_SHOW": "Kelmadi",
            "status.WAITING": "Kutmoqda",
            "status.INVITED": "Chaqirildi",
            "status.IN_SERVICE": "Xizmatda",
            "status.DONE": "Bajarildi",
        },
        "ru": {
            "status.PENDING": "Ожидание",
            "status.SCHEDULED": "Запланировано",
            "status.CONFIRMED": "Подтверждено",
            "status.IN_PROGRESS": "В процессе",
            "status.COMPLETED": "Завершено",
            "status.CANCELLED": "Отменено",
            "status.NO_SHOW": "Не явился",
            "status.WAITING": "Ожидает",
            "status.INVITED": "Приглашён",
            "status.IN_SERVICE": "На обслуживании",
            "status.DONE": "Выполнено",
        },
        "en": {
            "status.PENDING": "Pending",
            "status.SCHEDULED": "Scheduled",
            "status.CONFIRMED": "Confirmed",
            "status.IN_PROGRESS": "In progress",
            "status.COMPLETED": "Completed",
            "status.CANCELLED": "Cancelled",
            "status.NO_SHOW": "No-show",
            "status.WAITING": "Waiting",
            "status.INVITED": "Invited",
            "status.IN_SERVICE": "In service",
            "status.DONE": "Done",
        },
    }
)


def _date_picker(label: str):
    """Sana tanlagich: ui.input + ui.menu ichida ui.date (NiceGUI andozasi)."""
    date_input = ui.input(label).props("outlined dense readonly").classes("w-full")
    with date_input.add_slot("append"):
        icon = ui.icon("edit_calendar").classes("cursor-pointer")
    with ui.menu() as menu:
        ui.date().bind_value(date_input)
    icon.on("click", menu.open)
    return date_input


def render(active_tab: str = "list") -> None:
    if not require_login():
        return

    # Joriy lokal bo'yicha ustun sarlavhalari — render() har chaqirilganda hisoblanadi.
    columns = [
        {"name": "title", "label": t("appointments.col_title"), "field": "title", "align": "left"},
        {"name": "start_at", "label": t("appointments.col_start"), "field": "start_at", "align": "left"},
        {"name": "end_at", "label": t("appointments.col_end"), "field": "end_at", "align": "left"},
        {"name": "location", "label": t("appointments.col_location"), "field": "location", "align": "left"},
        {"name": "status", "label": t("common.status"), "field": "status", "align": "left"},
    ]
    status_label_map = {status: t(f"status.{status}") for status in APPOINTMENT_STATUSES}

    with shell(active="/appointments"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label(t("nav.appointments")).classes("text-2xl font-bold")
            can_manage = state.has_permission("appointments.manage")
            book_btn = ui.button(t("appointments.book"), icon="add", on_click=lambda: _open_book_dialog(reload_list))
            book_btn.props("unelevated color=indigo-7")
            book_btn.set_visibility(can_manage)

        with ui.tabs().classes("w-full") as tabs:
            ui.tab("list", label=t("appointments.tab_list"))
            ui.tab("queue", label=t("appointments.tab_queue"))

        with ui.tab_panels(tabs, value=active_tab).classes("w-full"):
            with ui.tab_panel("list"):
                table = ui.table(columns=columns, rows=[], row_key="id").classes("w-full sp-card").props("flat bordered")
                table.add_slot(
                    "body-cell-status",
                    r"""
                    <q-td :props="props">
                        <q-badge :color="['COMPLETED'].includes(props.value) ? 'green' :
                            (['CANCELLED', 'NO_SHOW'].includes(props.value) ? 'red' :
                            (['PENDING'].includes(props.value) ? 'grey' : 'blue'))">
                            {{ ("""
                    + json.dumps(status_label_map, ensure_ascii=False)
                    + r""")[props.value] || props.value }}
                        </q-badge>
                    </q-td>
                    """,
                )
                table.on("rowClick", lambda e: _open_detail_dialog(e.args[1]["id"], reload_list))
                info_row = ui.row().classes("items-center justify-between w-full")

                async def reload_list() -> None:
                    now = datetime.utcnow()
                    frm = now - timedelta(days=7)
                    to = now + timedelta(days=30)
                    try:
                        items = await state.client().list_appointments(frm.isoformat(), to.isoformat())
                    except ApiError as exc:
                        ui.notify(exc.message, type="negative")
                        return
                    table.rows = items
                    info_row.clear()
                    with info_row:
                        ui.label(f"{t('common.total')}: {len(items)} · {t('appointments.total_period')}")
                        ui.button(t("appointments.refresh"), icon="refresh", on_click=reload_list).props("flat dense")

                ui.timer(0.05, reload_list, once=True)

            with ui.tab_panel("queue"):
                _render_queue_tab()

        tabs.set_value(active_tab)


def _render_queue_tab() -> None:
    with ui.row().classes("w-full items-end gap-2 q-mb-sm"):
        join_assignee = ui.input(t("appointments.join_assignee_placeholder")).props("outlined dense").classes("col")
        join_client = ui.input(t("appointments.join_client_placeholder")).props("outlined dense").classes("col")

        async def join() -> None:
            try:
                await state.client().queue_join(
                    assignee_id=join_assignee.value or None, client_id=join_client.value or None
                )
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            ui.notify(t("appointments.joined_queue_notify"), type="positive")
            await reload_board()

        ui.button(t("appointments.join_queue_btn"), icon="how_to_reg", on_click=join).props("unelevated color=indigo-7")
        ui.button(t("appointments.refresh"), icon="refresh", on_click=lambda: reload_board()).props("flat")

    board_row = ui.row().classes("w-full gap-3 items-start")

    async def reload_board() -> None:
        try:
            board = await state.client().queue_board()
        except ApiError as exc:
            ui.notify(exc.message, type="negative")
            return
        board_row.clear()
        with board_row:
            for status_key in QUEUE_STATUS_KEYS:
                label = t(f"status.{status_key}")
                entries = board.get(status_key, [])
                with ui.column().classes("sp-card bg-white q-pa-sm").style("min-width:200px; max-width:240px;"):
                    ui.label(f"{label} ({len(entries)})").classes("text-sm font-bold q-mb-xs")
                    if not entries:
                        ui.label(t("appointments.queue_empty")).classes("text-caption text-grey-5")
                    for e in entries:
                        with ui.row().classes("items-center justify-between w-full q-py-xs"):
                            ui.label(f"№{e.get('number')}").classes("text-sm font-medium")
                            next_status = QUEUE_FLOW.get(status_key)
                            if next_status and state.has_permission("appointments.manage"):
                                async def advance(entry=e, nxt=next_status) -> None:
                                    try:
                                        await state.client().queue_update_status(entry["id"], nxt)
                                    except ApiError as exc:
                                        ui.notify(exc.message, type="negative")
                                        return
                                    await reload_board()

                                ui.button(icon="arrow_forward", on_click=advance).props(
                                    "flat dense round size=sm color=indigo-7"
                                )

    ui.timer(0.05, reload_board, once=True)


def _open_book_dialog(on_saved) -> None:
    kind_labels = {
        None: t("appointments.kind_all"),
        "LAWYER": t("appointments.kind_lawyer"),
        "ADVOCATE": t("appointments.kind_advocate"),
        "STAFF": t("appointments.kind_staff"),
    }
    specialist_kinds = {key: kind_labels[key] for key in SPECIALIST_KIND_KEYS}

    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:480px; max-width:640px;"):
        ui.label(t("appointments.book_dialog_title")).classes("text-lg font-bold")
        state_data: dict = {"selected_slot": None}

        with ui.row().classes("w-full gap-2 items-end"):
            kind_select = ui.select(specialist_kinds, value=None, label=t("appointments.specialist_kind_label")).props(
                "outlined dense"
            ).classes("col")
            search_input = ui.input(t("appointments.search_by_name")).props("outlined dense").classes("col")

        specialist_select = ui.select({}, label=t("appointments.specialist_label")).props("outlined dense").classes("w-full")

        async def load_specialists() -> None:
            try:
                rows = await state.client().list_specialists(kind=kind_select.value, search=search_input.value or None)
            except ApiError as exc:
                err.text = exc.message
                return
            options = {}
            for r in rows:
                user = r.get("user") or {}
                profile = user.get("profile") or {}
                name = f"{profile.get('last_name', '')} {profile.get('first_name', '')}".strip() or (r.get("id") or "")[:8]
                uid = user.get("id")
                if uid:
                    options[uid] = f"{name} ({r.get('kind')})"
            specialist_select.options = options
            specialist_select.update()

        ui.button(t("appointments.search_specialists_btn"), on_click=load_specialists).props("flat color=indigo-7")

        date_input = _date_picker(t("appointments.date_label"))
        slot_label = ui.label(t("appointments.no_time_selected")).classes("text-caption text-grey-6")
        slots_container = ui.column().classes("w-full gap-1")

        async def load_availability() -> None:
            slots_container.clear()
            state_data["selected_slot"] = None
            slot_label.text = t("appointments.no_time_selected")
            if not specialist_select.value or not date_input.value:
                err.text = t("appointments.select_specialist_and_date_first")
                return
            err.text = ""
            try:
                data = await state.client().get_availability(specialist_select.value, date_input.value)
            except ApiError as exc:
                err.text = exc.message
                return
            slots = data.get("slots") or []
            with slots_container:
                if not slots:
                    ui.label(t("appointments.no_slots")).classes("text-caption text-grey-5")
                with ui.row().classes("gap-1").style("flex-wrap:wrap;"):
                    for s in slots:
                        label = s["start_at"][11:16]

                        def pick(s=s, label=label) -> None:
                            state_data["selected_slot"] = s
                            slot_label.text = (
                                f"{t('appointments.selected_time_prefix')}: "
                                f"{s['start_at'][:16].replace('T', ' ')} - {s['end_at'][11:16]}"
                            )

                        ui.button(label, on_click=pick).props("outline dense color=indigo-7")

        ui.button(t("appointments.view_availability_btn"), on_click=load_availability).props("flat")

        title = ui.input(t("appointments.title_field")).props("outlined dense").classes("w-full")
        location = ui.input(t("appointments.col_location")).props("outlined dense").classes("w-full")
        client_id = ui.input(t("appointments.client_id_field")).props("outlined dense").classes("w-full")
        case_id = ui.input(t("appointments.case_id_field")).props("outlined dense").classes("w-full")
        err = ui.label("").classes("text-red-6 text-caption")

        async def save() -> None:
            if not specialist_select.value or not state_data["selected_slot"] or not title.value:
                err.text = t("appointments.required_fields_err")
                return
            slot = state_data["selected_slot"]
            payload = {
                "assignee_id": specialist_select.value,
                "title": title.value,
                "start_at": slot["start_at"],
                "end_at": slot["end_at"],
                "location": location.value or None,
                "case_id": case_id.value or None,
                "client_id": client_id.value or None,
            }
            try:
                await state.client().book_appointment(payload)
            except ApiError as exc:
                err.text = exc.message
                return
            ui.notify(t("appointments.booked_notify"), type="positive")
            dialog.close()
            await on_saved()

        with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
            ui.button(t("common.cancel"), on_click=dialog.close).props("flat")
            ui.button(t("common.save"), on_click=save).props("unelevated color=indigo-7")
    dialog.open()


def _open_detail_dialog(appointment_id: str, on_changed) -> None:
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:480px; max-width:640px;"):
        content = ui.column().classes("w-full gap-2")
        with content:
            ui.spinner()

        async def load() -> None:
            try:
                data = await state.client().get("appointments", appointment_id)
            except ApiError as exc:
                content.clear()
                with content:
                    ui.label(exc.message).classes("text-red-6")
                return
            content.clear()
            with content:
                with ui.row().classes("items-center justify-between w-full"):
                    ui.label(data.get("title", "")).classes("text-xl font-bold")
                    status_value = data.get("status", "")
                    ui.badge(t(f"status.{status_value}") if status_value else "").classes("q-px-sm")
                ui.label(f"{t('appointments.col_start')}: {(data.get('start_at') or '')[:16].replace('T', ' ')}")
                ui.label(f"{t('appointments.col_end')}: {(data.get('end_at') or '')[:16].replace('T', ' ')}")
                ui.label(f"{t('appointments.col_location')}: {data.get('location') or '—'}")
                ui.label(f"{t('appointments.client_id_field')}: {data.get('client_id') or '—'}")
                ui.label(f"{t('appointments.case_id_field')}: {data.get('case_id') or '—'}")

                if state.has_permission("appointments.manage"):
                    ui.separator().classes("q-my-sm")
                    status_options = {status: t(f"status.{status}") for status in APPOINTMENT_STATUSES}
                    status_select = ui.select(
                        status_options, value=data.get("status"), label=t("appointments.change_status_label")
                    ).props("outlined dense").classes("w-full")

                    async def change_status() -> None:
                        try:
                            await state.client().update_appointment_status(appointment_id, status_select.value)
                        except ApiError as exc:
                            ui.notify(exc.message, type="negative")
                            return
                        ui.notify(t("appointments.status_updated_notify"), type="positive")
                        await load()
                        await on_changed()

                    ui.button(t("appointments.save_status_btn"), on_click=change_status).props("flat color=indigo-7")

                with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
                    ui.button(t("common.close"), on_click=dialog.close).props("flat")

        ui.timer(0.05, load, once=True)
    dialog.open()
