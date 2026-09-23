from __future__ import annotations

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

BOARD_STATUS_KEYS = ["TODO", "IN_PROGRESS", "DONE"]
EXTRA_STATUSES = ["OVERDUE", "CANCELLED"]  # board() ustunlariga kirmaydi — alohida "Boshqa" ustunida ko'rsatiladi
ALL_STATUSES = ["TODO", "IN_PROGRESS", "DONE", "OVERDUE", "CANCELLED"]
PRIORITIES = ["LOW", "MEDIUM", "HIGH", "URGENT"]
PRIORITY_COLORS = {"LOW": "grey-7", "MEDIUM": "info", "HIGH": "warning", "URGENT": "negative"}

register(
    {
        "uz": {
            "tasks.new_task_btn": "Yangi vazifa",
            "tasks.col_other": "Boshqa (muddati o'tgan / bekor qilingan)",
            "tasks.col_empty": "Bo'sh",
            "tasks.due_prefix": "Muddat",
            "tasks.assignee_prefix": "Ijrochi",
            "tasks.priority_label": "Muhimlik",
            "tasks.description_field": "Tavsif",
            "tasks.assignee_id_field": "Ijrochi ID",
            "tasks.case_id_field": "Ish ID",
            "tasks.client_id_field": "Mijoz ID",
            "tasks.title_field": "Sarlavha *",
            "tasks.due_date_field": "Muddat",
            "tasks.title_required_err": "Sarlavha majburiy",
            "tasks.created_notify": "Vazifa yaratildi",
            "tasks.status_updated_notify": "Holat yangilandi",
            "tasks.deleted_notify": "Vazifa o'chirildi",
        },
        "ru": {
            "tasks.new_task_btn": "Новая задача",
            "tasks.col_other": "Другое (просроченные / отменённые)",
            "tasks.col_empty": "Пусто",
            "tasks.due_prefix": "Срок",
            "tasks.assignee_prefix": "Исполнитель",
            "tasks.priority_label": "Приоритет",
            "tasks.description_field": "Описание",
            "tasks.assignee_id_field": "ID исполнителя",
            "tasks.case_id_field": "ID дела",
            "tasks.client_id_field": "ID клиента",
            "tasks.title_field": "Заголовок *",
            "tasks.due_date_field": "Срок",
            "tasks.title_required_err": "Заголовок обязателен",
            "tasks.created_notify": "Задача создана",
            "tasks.status_updated_notify": "Статус обновлён",
            "tasks.deleted_notify": "Задача удалена",
        },
        "en": {
            "tasks.new_task_btn": "New task",
            "tasks.col_other": "Other (overdue / cancelled)",
            "tasks.col_empty": "Empty",
            "tasks.due_prefix": "Due date",
            "tasks.assignee_prefix": "Assignee",
            "tasks.priority_label": "Priority",
            "tasks.description_field": "Description",
            "tasks.assignee_id_field": "Assignee ID",
            "tasks.case_id_field": "Case ID",
            "tasks.client_id_field": "Client ID",
            "tasks.title_field": "Title *",
            "tasks.due_date_field": "Due date",
            "tasks.title_required_err": "Title is required",
            "tasks.created_notify": "Task created",
            "tasks.status_updated_notify": "Status updated",
            "tasks.deleted_notify": "Task deleted",
        },
    }
)

# Enum display strings shared across modules under the `status.*` namespace.
register(
    {
        "uz": {
            "status.TODO": "Rejalashtirilgan",
            "status.IN_PROGRESS": "Jarayonda",
            "status.DONE": "Bajarilgan",
            "status.OVERDUE": "Muddati o'tgan",
            "status.CANCELLED": "Bekor qilingan",
            "status.LOW": "Past",
            "status.MEDIUM": "O'rta",
            "status.HIGH": "Yuqori",
            "status.URGENT": "Shoshilinch",
        },
        "ru": {
            "status.TODO": "К выполнению",
            "status.IN_PROGRESS": "В процессе",
            "status.DONE": "Выполнено",
            "status.OVERDUE": "Просрочено",
            "status.CANCELLED": "Отменено",
            "status.LOW": "Низкий",
            "status.MEDIUM": "Средний",
            "status.HIGH": "Высокий",
            "status.URGENT": "Срочный",
        },
        "en": {
            "status.TODO": "To do",
            "status.IN_PROGRESS": "In progress",
            "status.DONE": "Done",
            "status.OVERDUE": "Overdue",
            "status.CANCELLED": "Cancelled",
            "status.LOW": "Low",
            "status.MEDIUM": "Medium",
            "status.HIGH": "High",
            "status.URGENT": "Urgent",
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


def render() -> None:
    if not require_login():
        return

    with shell(active="/tasks"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label(t("nav.tasks")).classes("text-2xl font-bold")
            can_create = state.has_permission("tasks.create")
            add_btn = ui.button(t("tasks.new_task_btn"), icon="add", on_click=lambda: _open_create_dialog(reload_board))
            add_btn.props("unelevated color=primary")
            add_btn.set_visibility(can_create)

        board_row = ui.row().classes("w-full gap-3 items-start").style("flex-wrap:wrap;")

        async def reload_board() -> None:
            try:
                board = await state.client().task_board()
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return

            extra_items: list[dict] = []
            for st in EXTRA_STATUSES:
                try:
                    result = await state.client().list_("tasks", {"status": st, "limit": 100, "page": 1})
                    extra_items.extend(result.get("items", []))
                except ApiError:
                    pass

            board_row.clear()
            with board_row:
                for status_key in BOARD_STATUS_KEYS:
                    _render_column(t(f"status.{status_key}"), board.get(status_key, []), reload_board, movable=True)
                _render_column(t("tasks.col_other"), extra_items, reload_board, movable=False)

        ui.timer(0.05, reload_board, once=True)


def _render_column(label: str, items: list[dict], on_changed, movable: bool) -> None:
    with ui.column().classes("sp-card bg-white q-pa-sm").style("min-width:270px; max-width:320px;"):
        ui.label(f"{label} ({len(items)})").classes("text-sm font-bold q-mb-xs")
        if not items:
            ui.label(t("tasks.col_empty")).classes("text-caption sp-subtle")
        for task in items:
            _render_card(task, on_changed, movable)


def _render_card(task: dict, on_changed, movable: bool) -> None:
    with ui.card().classes("w-full q-pa-sm q-mb-xs"):
        with ui.row().classes("items-center justify-between w-full cursor-pointer").on(
            "click", lambda task_=task: _open_detail_dialog(task_, on_changed)
        ):
            ui.label(task.get("title", "")).classes("text-sm font-medium")
            priority_value = task.get("priority", "")
            ui.badge(t(f"status.{priority_value}") if priority_value else "").props(
                f"color={PRIORITY_COLORS.get(task.get('priority'), 'grey')}"
            )
        due = task.get("due_date")
        ui.label(f"{t('tasks.due_prefix')}: {due[:10] if due else '—'}").classes("text-caption sp-muted")
        assignee_id = task.get("assignee_id")
        ui.label(f"{t('tasks.assignee_prefix')}: {(assignee_id[:8] + '…') if assignee_id else '—'}").classes(
            "text-caption sp-muted"
        )

        if movable and state.has_permission("tasks.update"):
            async def move(e, task_=task) -> None:
                try:
                    await state.client().move_task(task_["id"], e.value)
                except ApiError as exc:
                    ui.notify(exc.message, type="negative")
                    return
                ui.notify(t("tasks.status_updated_notify"), type="positive")
                await on_changed()

            status_options = {status: t(f"status.{status}") for status in ALL_STATUSES}
            ui.select(status_options, value=task.get("status"), label=t("common.status"), on_change=move).props(
                "outlined dense"
            ).classes("w-full q-mt-xs")


def _open_create_dialog(on_saved) -> None:
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:420px;"):
        ui.label(t("tasks.new_task_btn")).classes("text-lg font-bold")
        title = ui.input(t("tasks.title_field")).props("outlined dense").classes("w-full")
        description = ui.textarea(t("tasks.description_field")).props("outlined dense").classes("w-full")
        assignee_id = ui.input(t("tasks.assignee_id_field")).props("outlined dense").classes("w-full")
        case_id = ui.input(t("tasks.case_id_field")).props("outlined dense").classes("w-full")
        client_id = ui.input(t("tasks.client_id_field")).props("outlined dense").classes("w-full")
        due_date = _date_picker(t("tasks.due_date_field"))
        priority_options = {p: t(f"status.{p}") for p in PRIORITIES}
        priority = ui.select(priority_options, value="MEDIUM", label=t("tasks.priority_label")).props(
            "outlined dense"
        ).classes("w-full")
        err = ui.label("").classes("text-negative text-caption")

        async def save() -> None:
            if not title.value:
                err.text = t("tasks.title_required_err")
                return
            payload = {
                "title": title.value,
                "description": description.value or None,
                "assignee_id": assignee_id.value or None,
                "case_id": case_id.value or None,
                "client_id": client_id.value or None,
                "due_date": f"{due_date.value}T00:00:00" if due_date.value else None,
                "priority": priority.value,
            }
            try:
                await state.client().create("tasks", payload)
            except ApiError as exc:
                err.text = exc.message
                return
            ui.notify(t("tasks.created_notify"), type="positive")
            dialog.close()
            await on_saved()

        with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
            ui.button(t("common.cancel"), on_click=dialog.close).props("flat")
            ui.button(t("common.save"), on_click=save).props("unelevated color=primary")
    dialog.open()


def _open_detail_dialog(task: dict, on_changed) -> None:
    # tasks routerida GET /tasks/{id} yo'q — shu sababli board/list qatoridan
    # kelgan to'liq ma'lumot (serialize() barcha maydonlarni qaytaradi) ishlatiladi.
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:480px; max-width:640px;"):
        with ui.row().classes("items-center justify-between w-full"):
            ui.label(task.get("title", "")).classes("text-xl font-bold")
            status_value = task.get("status", "")
            ui.badge(t(f"status.{status_value}") if status_value else "").classes("q-px-sm")
        priority_value = task.get("priority", "")
        ui.label(f"{t('tasks.priority_label')}: {t(f'status.{priority_value}') if priority_value else '—'}")
        due = task.get("due_date")
        ui.label(f"{t('tasks.due_prefix')}: {due[:10] if due else '—'}")
        ui.label(f"{t('tasks.description_field')}: {task.get('description') or '—'}")
        ui.label(f"{t('tasks.assignee_id_field')}: {task.get('assignee_id') or '—'}")
        ui.label(f"{t('tasks.case_id_field')}: {task.get('case_id') or '—'}")
        ui.label(f"{t('tasks.client_id_field')}: {task.get('client_id') or '—'}")
        err = ui.label("").classes("text-negative text-caption")

        with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
            if state.has_permission("tasks.delete"):
                async def remove() -> None:
                    try:
                        await state.client().delete("tasks", task["id"])
                    except ApiError as exc:
                        err.text = exc.message
                        return
                    ui.notify(t("tasks.deleted_notify"), type="positive")
                    dialog.close()
                    await on_changed()

                ui.button(t("common.delete"), on_click=remove).props("flat color=negative")
            ui.button(t("common.close"), on_click=dialog.close).props("flat")
    dialog.open()
