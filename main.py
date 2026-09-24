"""ShahPremium — NiceGUI frontend kirish nuqtasi.

Ishga tushirish:  .venv\\Scripts\\python.exe main.py
Backend manzili (FastAPI): SHAHPREMIUM_API_URL muhit o'zgaruvchisi orqali
sozlanadi (standart: http://127.0.0.1:4000/api/v1).
"""

from __future__ import annotations

import os

from nicegui import app, ui

from app.theme import apply_app_colors
from app.pages import (
    appointments,
    audit,
    cases,
    chat,
    clients,
    contracts,
    dashboard,
    documents,
    employees,
    integrations,
    login,
    notifications,
    offices,
    payments,
    permissions,
    regions,
    reports,
    roles,
    services,
    settings,
    specialists,
    tasks,
    users,
)


@ui.page("/specialists")
def _specialists_page() -> None:
    specialists.render()


@ui.page("/login")
def _login_page() -> None:
    login.render()


@ui.page("/")
def _dashboard_page() -> None:
    dashboard.render()


@ui.page("/clients")
def _clients_page() -> None:
    clients.render()


@ui.page("/cases")
def _cases_page() -> None:
    cases.render()


@ui.page("/contracts")
def _contracts_page() -> None:
    contracts.render()


@ui.page("/documents")
def _documents_page() -> None:
    documents.render()


@ui.page("/employees")
def _employees_page() -> None:
    employees.render()


@ui.page("/regions")
def _regions_page() -> None:
    regions.render()


@ui.page("/offices")
def _offices_page() -> None:
    offices.render()


@ui.page("/services")
def _services_page() -> None:
    services.render()


@ui.page("/appointments")
def _appointments_page() -> None:
    appointments.render()


@ui.page("/appointments/queue")
def _appointments_queue_page() -> None:
    appointments.render(active_tab="queue")


@ui.page("/tasks")
def _tasks_page() -> None:
    tasks.render()


@ui.page("/payments")
def _payments_page() -> None:
    payments.render()


@ui.page("/reports")
def _reports_page() -> None:
    reports.render()


@ui.page("/users")
def _users_page() -> None:
    users.render()


@ui.page("/roles")
def _roles_page() -> None:
    roles.render()


@ui.page("/permissions")
def _permissions_page() -> None:
    permissions.render()


@ui.page("/notifications")
def _notifications_page() -> None:
    notifications.render()


@ui.page("/chat")
def _chat_page() -> None:
    chat.render()


@ui.page("/audit")
def _audit_page() -> None:
    audit.render()


@ui.page("/integrations")
def _integrations_page() -> None:
    integrations.render()


@ui.page("/settings")
def _settings_page() -> None:
    settings.render()


apply_app_colors()
app.add_static_files("/assets", "assets")

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="ShahPremium",
        favicon="assets/favicon.ico",
        storage_secret=os.environ.get("SHAHPREMIUM_STORAGE_SECRET", "dev-storage-secret-change-me"),
        # Render/Railway kabi PaaS'lar portni `$PORT` orqali beradi.
        port=int(os.environ.get("PORT", os.environ.get("SHAHPREMIUM_FRONTEND_PORT", "8080"))),
        reload=False,
        show=False,
    )
