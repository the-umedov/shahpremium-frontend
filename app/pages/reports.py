from __future__ import annotations

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

REPORT_TYPE_KEYS = ["payments", "income", "expense", "debt", "clients", "employees", "services", "cases"]
EXPORT_FORMATS = ["csv", "xlsx", "pdf"]

register(
    {
        "uz": {
            "reports.no_access": "Ushbu bo'limni ko'rish uchun ruxsatingiz yo'q",
            "reports.type": "Hisobot turi",
            "reports.date_from": "Sanadan (YYYY-MM-DD)",
            "reports.date_to": "Sanagacha (YYYY-MM-DD)",
            "reports.client_id": "Mijoz ID (ixtiyoriy)",
            "reports.region_id": "Hudud ID (ixtiyoriy)",
            "reports.employee_id": "Xodim ID (ixtiyoriy)",
            "reports.service_id": "Xizmat ID (ixtiyoriy)",
            "reports.show": "Ko'rsatish",
            "reports.export_prefix": "Eksport",
            "report_type.payments": "To'lovlar",
            "report_type.income": "Daromad",
            "report_type.expense": "Xarajat",
            "report_type.debt": "Qarzdorlik",
            "report_type.clients": "Mijozlar",
            "report_type.employees": "Xodimlar",
            "report_type.services": "Xizmatlar",
            "report_type.cases": "Ishlar",
            "export_format.csv": "CSV",
            "export_format.xlsx": "Excel",
            "export_format.pdf": "PDF",
        },
        "ru": {
            "reports.no_access": "У вас нет прав для просмотра этого раздела",
            "reports.type": "Тип отчёта",
            "reports.date_from": "С даты (YYYY-MM-DD)",
            "reports.date_to": "По дату (YYYY-MM-DD)",
            "reports.client_id": "ID клиента (необязательно)",
            "reports.region_id": "ID региона (необязательно)",
            "reports.employee_id": "ID сотрудника (необязательно)",
            "reports.service_id": "ID услуги (необязательно)",
            "reports.show": "Показать",
            "reports.export_prefix": "Экспорт",
            "report_type.payments": "Платежи",
            "report_type.income": "Доход",
            "report_type.expense": "Расход",
            "report_type.debt": "Задолженность",
            "report_type.clients": "Клиенты",
            "report_type.employees": "Сотрудники",
            "report_type.services": "Услуги",
            "report_type.cases": "Дела",
            "export_format.csv": "CSV",
            "export_format.xlsx": "Excel",
            "export_format.pdf": "PDF",
        },
        "en": {
            "reports.no_access": "You do not have permission to view this section",
            "reports.type": "Report type",
            "reports.date_from": "From date (YYYY-MM-DD)",
            "reports.date_to": "To date (YYYY-MM-DD)",
            "reports.client_id": "Client ID (optional)",
            "reports.region_id": "Region ID (optional)",
            "reports.employee_id": "Employee ID (optional)",
            "reports.service_id": "Service ID (optional)",
            "reports.show": "Show",
            "reports.export_prefix": "Export",
            "report_type.payments": "Payments",
            "report_type.income": "Income",
            "report_type.expense": "Expense",
            "report_type.debt": "Debt",
            "report_type.clients": "Clients",
            "report_type.employees": "Employees",
            "report_type.services": "Services",
            "report_type.cases": "Cases",
            "export_format.csv": "CSV",
            "export_format.xlsx": "Excel",
            "export_format.pdf": "PDF",
        },
    }
)


def render() -> None:
    if not require_login():
        return

    report_types = [(key, t(f"report_type.{key}")) for key in REPORT_TYPE_KEYS]

    with shell(active="/reports"):
        ui.label(t("nav.reports")).classes("text-2xl font-bold")

        if not state.has_permission("reports.read"):
            ui.label(t("reports.no_access")).classes("text-red-6")
            return

        with ui.row().classes("w-full items-end gap-2"):
            type_select = ui.select(
                {key: label for key, label in report_types}, value=report_types[0][0], label=t("reports.type")
            ).props("outlined dense").classes("w-56")
            date_from = ui.input(t("reports.date_from")).props("outlined dense").classes("w-48")
            date_to = ui.input(t("reports.date_to")).props("outlined dense").classes("w-48")
            client_id = ui.input(t("reports.client_id")).props("outlined dense").classes("w-48")
            region_id = ui.input(t("reports.region_id")).props("outlined dense").classes("w-40")
            employee_id = ui.input(t("reports.employee_id")).props("outlined dense").classes("w-40")
            service_id = ui.input(t("reports.service_id")).props("outlined dense").classes("w-40")

        with ui.row().classes("items-center gap-2"):
            ui.button(t("reports.show"), icon="visibility", on_click=lambda: show_report()).props(
                "unelevated color=indigo-7"
            )
            can_export = state.has_permission("reports.export")
            for fmt in EXPORT_FORMATS:
                btn = ui.button(
                    f"{t('reports.export_prefix')} ({t(f'export_format.{fmt}')})",
                    icon="download",
                    on_click=lambda f=fmt: do_export(f),
                )
                btn.props("flat color=indigo-7")
                btn.set_visibility(can_export)

        title_label = ui.label("").classes("text-lg font-semibold")
        err_label = ui.label("").classes("text-red-6 text-caption")
        table = ui.table(columns=[], rows=[], row_key="_row").classes("w-full sp-card").props("flat bordered")

        def _params() -> dict:
            return {
                "date_from": date_from.value or None,
                "date_to": date_to.value or None,
                "client_id": client_id.value or None,
                "region_id": region_id.value or None,
                "employee_id": employee_id.value or None,
                "service_id": service_id.value or None,
            }

        async def show_report() -> None:
            err_label.text = ""
            try:
                data = await state.client().get_report(type_select.value, _params())
            except ApiError as exc:
                err_label.text = exc.message
                return
            title_label.text = data.get("title", "")
            columns = [
                {"name": c["key"], "label": c["header"], "field": c["key"], "align": "left"}
                for c in data.get("columns", [])
            ]
            rows = data.get("rows", [])
            for i, r in enumerate(rows):
                r["_row"] = i
            table.columns = columns
            table.rows = rows
            table.update()

        async def do_export(fmt: str) -> None:
            err_label.text = ""
            try:
                content, filename = await state.client().export_report(type_select.value, fmt, _params())
            except ApiError as exc:
                err_label.text = exc.message
                return
            ui.download(content, filename)

        ui.timer(0.05, show_report, once=True)
