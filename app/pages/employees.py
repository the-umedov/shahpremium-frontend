from __future__ import annotations

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

EMPLOYEE_KINDS = ["LAWYER", "ADVOCATE", "STAFF"]
EMPLOYEE_STATUSES = ["ACTIVE", "INACTIVE", "ON_VACATION", "BUSY", "UNAVAILABLE"]

register(
    {
        "uz": {
            "employees.search": "Qidirish (ism)",
            "employees.kind": "Turi",
            "employees.all": "Barchasi",
            "employees.total": "Jami: {n} ta",
            "employees.full_name": "F.I.Sh.",
            "employees.position": "Lavozim",
            "employees.office": "Ofis",
            "employees.specialization": "Mutaxassislik",
            "employees.education": "Ta'lim",
            "employees.experience_years": "Tajriba (yil)",
            "employees.languages": "Tillar",
            "employees.hire_date": "Ishga qabul sanasi",
            "employees.commission_percent": "Komissiya foizi",
            "employees.commission_earned": "Topilgan komissiya",
            "employees.detail_line": "Turi: {kind} · Lavozim: {position}",
            "employees.specialization_line": "Mutaxassislik: {value}",
            "employees.experience_line": "Tajriba: {value} yil",
            "employees.education_line": "Ta'lim: {value}",
            "employees.languages_line": "Tillar: {value}",
            "employees.office_line": "Ofis: {value}",
            "employees.hire_date_line": "Ishga qabul sanasi: {value}",
            "employees.commission_line": "Komissiya foizi: {value}%",
            "employees.commission_percent_input": "Komissiya (%)",
            "employees.save_commission": "Komissiyani saqlash",
            "employees.schedule_title": "Ish grafigi (haftalik)",
            "employees.works": "Ishlaydi",
            "employees.start_time": "Boshlanish",
            "employees.end_time": "Tugash",
            "employees.save_schedule": "Grafikni saqlash",
            "employees.updated": "Xodim ma'lumotlari yangilandi",
            "employees.commission_updated": "Komissiya foizi yangilandi",
            "employees.schedule_saved": "Ish grafigi saqlandi",
            "employees.day_mon": "Dushanba",
            "employees.day_tue": "Seshanba",
            "employees.day_wed": "Chorshanba",
            "employees.day_thu": "Payshanba",
            "employees.day_fri": "Juma",
            "employees.day_sat": "Shanba",
            "employees.day_sun": "Yakshanba",
            "status.LAWYER": "Yurist",
            "status.ADVOCATE": "Advokat",
            "status.STAFF": "Xodim",
            "status.ACTIVE": "Faol",
            "status.INACTIVE": "Nofaol",
            "status.ON_VACATION": "Ta'tilda",
            "status.BUSY": "Band",
            "status.UNAVAILABLE": "Mavjud emas",
        },
        "ru": {
            "employees.search": "Поиск (имя)",
            "employees.kind": "Тип",
            "employees.all": "Все",
            "employees.total": "Всего: {n}",
            "employees.full_name": "ФИО",
            "employees.position": "Должность",
            "employees.office": "Офис",
            "employees.specialization": "Специализация",
            "employees.education": "Образование",
            "employees.experience_years": "Опыт (лет)",
            "employees.languages": "Языки",
            "employees.hire_date": "Дата приёма на работу",
            "employees.commission_percent": "Процент комиссии",
            "employees.commission_earned": "Заработанная комиссия",
            "employees.detail_line": "Тип: {kind} · Должность: {position}",
            "employees.specialization_line": "Специализация: {value}",
            "employees.experience_line": "Опыт: {value} лет",
            "employees.education_line": "Образование: {value}",
            "employees.languages_line": "Языки: {value}",
            "employees.office_line": "Офис: {value}",
            "employees.hire_date_line": "Дата приёма на работу: {value}",
            "employees.commission_line": "Процент комиссии: {value}%",
            "employees.commission_percent_input": "Комиссия (%)",
            "employees.save_commission": "Сохранить комиссию",
            "employees.schedule_title": "Рабочий график (недельный)",
            "employees.works": "Работает",
            "employees.start_time": "Начало",
            "employees.end_time": "Конец",
            "employees.save_schedule": "Сохранить график",
            "employees.updated": "Данные сотрудника обновлены",
            "employees.commission_updated": "Процент комиссии обновлён",
            "employees.schedule_saved": "График сохранён",
            "employees.day_mon": "Понедельник",
            "employees.day_tue": "Вторник",
            "employees.day_wed": "Среда",
            "employees.day_thu": "Четверг",
            "employees.day_fri": "Пятница",
            "employees.day_sat": "Суббота",
            "employees.day_sun": "Воскресенье",
            "status.LAWYER": "Юрист",
            "status.ADVOCATE": "Адвокат",
            "status.STAFF": "Сотрудник",
            "status.ACTIVE": "Активен",
            "status.INACTIVE": "Неактивен",
            "status.ON_VACATION": "В отпуске",
            "status.BUSY": "Занят",
            "status.UNAVAILABLE": "Недоступен",
        },
        "en": {
            "employees.search": "Search (name)",
            "employees.kind": "Type",
            "employees.all": "All",
            "employees.total": "Total: {n}",
            "employees.full_name": "Full name",
            "employees.position": "Position",
            "employees.office": "Office",
            "employees.specialization": "Specialization",
            "employees.education": "Education",
            "employees.experience_years": "Experience (years)",
            "employees.languages": "Languages",
            "employees.hire_date": "Hire date",
            "employees.commission_percent": "Commission percent",
            "employees.commission_earned": "Commission earned",
            "employees.detail_line": "Type: {kind} · Position: {position}",
            "employees.specialization_line": "Specialization: {value}",
            "employees.experience_line": "Experience: {value} years",
            "employees.education_line": "Education: {value}",
            "employees.languages_line": "Languages: {value}",
            "employees.office_line": "Office: {value}",
            "employees.hire_date_line": "Hire date: {value}",
            "employees.commission_line": "Commission percent: {value}%",
            "employees.commission_percent_input": "Commission (%)",
            "employees.save_commission": "Save commission",
            "employees.schedule_title": "Weekly work schedule",
            "employees.works": "Works",
            "employees.start_time": "Start",
            "employees.end_time": "End",
            "employees.save_schedule": "Save schedule",
            "employees.updated": "Employee data updated",
            "employees.commission_updated": "Commission percent updated",
            "employees.schedule_saved": "Schedule saved",
            "employees.day_mon": "Monday",
            "employees.day_tue": "Tuesday",
            "employees.day_wed": "Wednesday",
            "employees.day_thu": "Thursday",
            "employees.day_fri": "Friday",
            "employees.day_sat": "Saturday",
            "employees.day_sun": "Sunday",
            "status.LAWYER": "Lawyer",
            "status.ADVOCATE": "Advocate",
            "status.STAFF": "Staff",
            "status.ACTIVE": "Active",
            "status.INACTIVE": "Inactive",
            "status.ON_VACATION": "On vacation",
            "status.BUSY": "Busy",
            "status.UNAVAILABLE": "Unavailable",
        },
    }
)


def _full_name(item: dict) -> str:
    user = item.get("user") or {}
    profile = user.get("profile") or {}
    name = f"{profile.get('first_name') or ''} {profile.get('last_name') or ''}".strip()
    return name or user.get("email") or user.get("phone") or "—"


def render() -> None:
    if not require_login():
        return

    columns = [
        {"name": "full_name", "label": t("employees.full_name"), "field": "full_name", "align": "left"},
        {"name": "kind", "label": t("employees.kind"), "field": "kind_label", "align": "left"},
        {"name": "status", "label": t("common.status"), "field": "status_label", "align": "left"},
        {"name": "position", "label": t("employees.position"), "field": "position", "align": "left"},
        {"name": "office_name", "label": t("employees.office"), "field": "office_name", "align": "left"},
    ]

    with shell(active="/employees"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label(t("nav.employees")).classes("text-2xl font-bold")

        with ui.row().classes("w-full items-end gap-2"):
            search = ui.input(t("employees.search")).props("outlined dense clearable").classes("col")
            kind_filter = ui.select(
                [t("employees.all")] + EMPLOYEE_KINDS, value=t("employees.all"), label=t("employees.kind")
            ).props("outlined dense").classes("col")
            status_filter = ui.select(
                [t("employees.all")] + EMPLOYEE_STATUSES, value=t("employees.all"), label=t("common.status")
            ).props("outlined dense").classes("col")

        table = ui.table(columns=columns, rows=[], row_key="id").classes("w-full sp-card").props("flat bordered")
        table.on("rowClick", lambda e: _open_detail_dialog(e.args[1]["id"], reload))
        pagination_row = ui.row().classes("items-center justify-between w-full")

        state_page = {"page": 1, "limit": 20, "total_pages": 1}

        async def reload() -> None:
            params = {"page": state_page["page"], "limit": state_page["limit"], "search": search.value}
            if kind_filter.value and kind_filter.value != t("employees.all"):
                params["kind"] = kind_filter.value
            if status_filter.value and status_filter.value != t("employees.all"):
                params["status"] = status_filter.value
            try:
                result = await state.client().list_("employees", params)
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            items = result.get("items", [])
            for it in items:
                it["full_name"] = _full_name(it)
                it["office_name"] = (it.get("office") or {}).get("name", "—")
                it["kind_label"] = t(f"status.{it.get('kind')}") if it.get("kind") else "—"
                it["status_label"] = t(f"status.{it.get('status')}") if it.get("status") else "—"
            table.rows = items
            meta = result.get("meta", {})
            state_page["total_pages"] = meta.get("total_pages", 1)
            pagination_row.clear()
            with pagination_row:
                ui.label(t("employees.total").format(n=meta.get("total", 0)))
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
        kind_filter.on_value_change(_reload_first_page)
        status_filter.on_value_change(_reload_first_page)
        ui.timer(0.05, reload, once=True)


def _open_detail_dialog(employee_id: str, on_changed) -> None:
    days_of_week = [
        (0, t("employees.day_mon")), (1, t("employees.day_tue")), (2, t("employees.day_wed")),
        (3, t("employees.day_thu")), (4, t("employees.day_fri")), (5, t("employees.day_sat")),
        (6, t("employees.day_sun")),
    ]

    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:600px; max-width:820px;"):
        content = ui.column().classes("w-full gap-2")
        with content:
            ui.spinner()

        async def load() -> None:
            try:
                data = await state.client().get("employees", employee_id)
            except ApiError as exc:
                content.clear()
                with content:
                    ui.label(exc.message).classes("text-negative")
                return
            content.clear()
            with content:
                kind_display = t(f"status.{data.get('kind')}") if data.get("kind") else "—"
                status_display = t(f"status.{data.get('status')}") if data.get("status") else "—"
                with ui.row().classes("items-center justify-between w-full"):
                    ui.label(_full_name(data)).classes("text-xl font-bold")
                    ui.badge(status_display).classes("q-px-sm")
                ui.label(
                    t("employees.detail_line").format(kind=kind_display, position=data.get("position") or "—")
                ).classes("text-caption sp-muted")

                with ui.row().classes("gap-6 q-mt-sm"):
                    ui.label(t("employees.specialization_line").format(value=data.get("specialization") or "—"))
                    ui.label(
                        t("employees.experience_line").format(
                            value=data.get("experience_years") if data.get("experience_years") is not None else "—"
                        )
                    )
                ui.label(t("employees.education_line").format(value=data.get("education") or "—"))
                ui.label(t("employees.languages_line").format(value=", ".join(data.get("languages") or []) or "—"))
                office = data.get("office") or {}
                ui.label(t("employees.office_line").format(value=office.get("name") or "—"))
                ui.label(t("employees.hire_date_line").format(value=data.get("hire_date") or "—"))
                ui.label(
                    t("employees.commission_line").format(
                        value=data.get("commission_percent") if data.get("commission_percent") is not None else "—"
                    )
                )

                stats = data.get("stats") or {}
                with ui.row().classes("gap-4 q-mt-md"):
                    for key, label in [
                        ("clients", t("nav.clients")), ("cases", t("nav.cases")),
                        ("contracts", t("nav.contracts")), ("tasks", t("nav.tasks")),
                    ]:
                        with ui.column().classes("items-center"):
                            ui.label(str(stats.get(key, 0))).classes("text-lg font-bold text-primary")
                            ui.label(label).classes("text-caption sp-muted")
                    with ui.column().classes("items-center"):
                        ui.label(f"{stats.get('commission_earned', 0):,}").classes("text-lg font-bold text-positive")
                        ui.label(t("employees.commission_earned")).classes("text-caption sp-muted")

                if state.has_permission("employees.update"):
                    ui.separator().classes("q-my-sm")
                    ui.label(t("common.edit")).classes("text-md font-semibold")

                    offices_list: list[dict] = []
                    try:
                        offices_result = await state.client().list_("offices", {})
                        offices_list = offices_result if isinstance(offices_result, list) else offices_result.get("items", [])
                    except ApiError:
                        offices_list = []
                    office_options = {o["id"]: o["name"] for o in offices_list}

                    with ui.row().classes("w-full gap-2"):
                        kind_sel = ui.select(EMPLOYEE_KINDS, value=data.get("kind"), label=t("employees.kind")).props(
                            "outlined dense"
                        ).classes("col")
                        status_sel = ui.select(EMPLOYEE_STATUSES, value=data.get("status"), label=t("common.status")).props(
                            "outlined dense"
                        ).classes("col")
                    with ui.row().classes("w-full gap-2"):
                        position_in = ui.input(t("employees.position"), value=data.get("position") or "").props(
                            "outlined dense"
                        ).classes("col")
                        specialization_in = ui.input(
                            t("employees.specialization"), value=data.get("specialization") or ""
                        ).props("outlined dense").classes("col")
                    with ui.row().classes("w-full gap-2"):
                        education_in = ui.input(t("employees.education"), value=data.get("education") or "").props(
                            "outlined dense"
                        ).classes("col")
                        experience_in = ui.number(
                            t("employees.experience_years"), value=data.get("experience_years")
                        ).props("outlined dense").classes("col")
                    office_sel = ui.select(
                        office_options, value=data.get("office_id"), label=t("employees.office")
                    ).props("outlined dense clearable").classes("w-full")
                    edit_err = ui.label("").classes("text-negative text-caption")

                    async def save_edit() -> None:
                        payload = {
                            "kind": kind_sel.value,
                            "status": status_sel.value,
                            "position": position_in.value or None,
                            "specialization": specialization_in.value or None,
                            "education": education_in.value or None,
                            "experience_years": int(experience_in.value) if experience_in.value not in (None, "") else None,
                            "office_id": office_sel.value or None,
                        }
                        try:
                            await state.client().update("employees", employee_id, payload)
                        except ApiError as exc:
                            edit_err.text = exc.message
                            return
                        ui.notify(t("employees.updated"), type="positive")
                        await load()
                        await on_changed()

                    ui.button(t("common.save"), on_click=save_edit).props("unelevated color=primary")

                    ui.separator().classes("q-my-sm")
                    ui.label(t("employees.commission_percent")).classes("text-md font-semibold")
                    with ui.row().classes("w-full items-end gap-2"):
                        commission_in = ui.number(
                            t("employees.commission_percent_input"), value=data.get("commission_percent")
                        ).props("outlined dense").classes("col")

                        async def save_commission() -> None:
                            if commission_in.value is None:
                                return
                            try:
                                await state.client().set_employee_commission(employee_id, float(commission_in.value))
                            except ApiError as exc:
                                ui.notify(exc.message, type="negative")
                                return
                            ui.notify(t("employees.commission_updated"), type="positive")
                            await load()

                        ui.button(t("employees.save_commission"), on_click=save_commission).props("flat color=primary")

                    ui.separator().classes("q-my-sm")
                    ui.label(t("employees.schedule_title")).classes("text-md font-semibold")
                    existing_schedule = {
                        s["day_of_week"]: s for s in ((data.get("user") or {}).get("schedules") or [])
                    }
                    day_inputs = {}
                    for day_idx, day_label in days_of_week:
                        existing = existing_schedule.get(day_idx, {})
                        with ui.row().classes("w-full items-center gap-2"):
                            ui.label(day_label).classes("w-28")
                            active_cb = ui.checkbox(t("employees.works"), value=bool(existing.get("is_active", False)))
                            start_in = ui.input(t("employees.start_time"), value=existing.get("start_time") or "09:00").props(
                                "outlined dense"
                            ).classes("w-28")
                            end_in = ui.input(t("employees.end_time"), value=existing.get("end_time") or "18:00").props(
                                "outlined dense"
                            ).classes("w-28")
                            day_inputs[day_idx] = (active_cb, start_in, end_in)
                    schedule_err = ui.label("").classes("text-negative text-caption")

                    async def save_schedule() -> None:
                        items = []
                        for day_idx, (active_cb, start_in, end_in) in day_inputs.items():
                            if not active_cb.value:
                                continue
                            items.append(
                                {
                                    "day_of_week": day_idx,
                                    "start_time": start_in.value,
                                    "end_time": end_in.value,
                                }
                            )
                        try:
                            await state.client().set_employee_schedule(employee_id, items)
                        except ApiError as exc:
                            schedule_err.text = exc.message
                            return
                        ui.notify(t("employees.schedule_saved"), type="positive")
                        await load()

                    ui.button(t("employees.save_schedule"), on_click=save_schedule).props("flat color=primary")

                with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
                    ui.button(t("common.close"), on_click=dialog.close).props("flat")

        ui.timer(0.05, load, once=True)
    dialog.open()
