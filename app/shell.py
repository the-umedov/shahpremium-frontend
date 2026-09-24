"""Umumiy sahifa qobig'i: header + chap navigatsiya paneli (barcha himoyalangan
sahifalarda takrorlanadigan qism). Light/Dark/System tema va uz/ru/en til
almashtirish shu yerda markazlashtirilgan (04_Design_System_i18n.md)."""

from __future__ import annotations

from nicegui import ui

from app import state
from app.i18n import LOCALE_LABELS, t
from app.theme import BRAND_OVERRIDE_CSS, INK

# (tarjima kaliti, yo'l, ikonka, ruxsat_yoki_None)
NAV_ITEMS = [
    ("nav.dashboard", "/", "dashboard", None),
    ("nav.employees", "/employees", "badge", "employees.read"),
    ("nav.services", "/services", "handyman", None),
    ("nav.clients", "/clients", "groups", "clients.read"),
    ("nav.cases", "/cases", "gavel", "cases.read"),
    ("nav.permissions", "/permissions", "vpn_key", "roles.manage"),
    ("nav.reports", "/reports", "bar_chart", "reports.read"),
    ("nav.contracts", "/contracts", "description", "contracts.read"),
    ("nav.documents", "/documents", "folder", "documents.read"),
    ("nav.appointments", "/appointments", "event", "appointments.manage"),
    ("nav.tasks", "/tasks", "checklist", "tasks.read"),
    ("nav.payments", "/payments", "payments", "payments.read"),
    ("nav.notifications", "/notifications", "notifications", "notifications.read"),
    ("nav.chat", "/chat", "forum", "chat.use"),
    ("nav.regions", "/regions", "map", None),
    ("nav.offices", "/offices", "apartment", None),
    ("nav.users", "/users", "manage_accounts", "users.read"),
    ("nav.roles", "/roles", "admin_panel_settings", "roles.manage"),
    ("nav.audit", "/audit", "history", "audit.read"),
    ("nav.integrations", "/integrations", "integration_instructions", "integrations.manage"),
    ("nav.settings", "/settings", "settings", None),
]

# Mijoz (CLIENT) menyusi: xizmatlar tepada, advokat/yuristlar alohida bo'lim,
# suhbatlar yo'q.
CLIENT_NAV_ITEMS = [
    ("nav.dashboard", "/", "dashboard", None),
    ("nav.services", "/services", "handyman", None),
    ("nav.specialists", "/specialists", "balance", "appointments.manage"),
    ("nav.cases", "/cases", "gavel", "cases.read"),
    ("nav.contracts", "/contracts", "description", "contracts.read"),
    ("nav.documents", "/documents", "folder", "documents.read"),
    ("nav.appointments", "/appointments", "event", "appointments.manage"),
    ("nav.payments", "/payments", "payments", "payments.read"),
    ("nav.notifications", "/notifications", "notifications", "notifications.read"),
    ("nav.regions", "/regions", "map", None),
    ("nav.offices", "/offices", "apartment", None),
    ("nav.settings", "/settings", "settings", None),
]

# Shu kenglikdan tor ekranda panel "overlay" (ustidan ochiladigan) rejimga o'tadi.
DRAWER_BREAKPOINT = 1024

PRIMARY = INK


def require_login() -> bool:
    """Token yo'q bo'lsa /login'ga yo'naltiradi. False qaytsa, sahifa chizilmasligi kerak."""
    if not state.is_authenticated():
        ui.navigate.to("/login")
        return False
    return True


def _apply_theme(dark_mode: ui.dark_mode) -> None:
    theme = state.get_theme()
    if theme == "dark":
        dark_mode.value = True
    elif theme == "light":
        dark_mode.value = False
    else:
        dark_mode.value = None  # 'system' — Quasar OS afzalligiga qarab avtomatik


async def _persist_preference(field: str, value: str) -> None:
    # Sozlamalar sahifasi ochilganda brauzer holatini backend'dagi qiymat bilan
    # sinxronlaydi — header'dagi tanlov backend'ga ham yozilmasa, mavzu/til
    # keyingi safar eski qiymatga "qaytib qolardi".
    try:
        await state.client().update_preferences({field: value})
    except Exception:  # noqa: BLE001 — UI darhol o'zgaradi, saqlash xatosi bloklamasin
        pass


async def _set_theme(dark_mode: ui.dark_mode, theme: str) -> None:
    state.set_theme(theme)
    _apply_theme(dark_mode)
    await _persist_preference("theme", theme)


async def _set_locale(locale: str) -> None:
    state.set_locale(locale)
    await _persist_preference("locale", locale)
    # t() render vaqtida baholanadi — yangi tilni butun sahifada qo'llash
    # uchun eng ishonchli yo'l to'liq qayta yuklash.
    ui.navigate.reload()


def shell(active: str = ""):
    """Header + drawer chizadi. Sahifa mazmuni uchun `with shell(...):` konteksti qaytaradi."""
    me = state.get_me() or {}

    ui.add_head_html(BRAND_OVERRIDE_CSS)

    dark_mode = ui.dark_mode()
    _apply_theme(dark_mode)

    # Telefon/planshetda (1024px dan tor ekranlarda) chap panel avtomatik
    # yashiriladi (overlay rejimi). Kompyuterda esa gamburger tugmasi panelni
    # butunlay yopmaydi — "mini" rejimga o'tkazadi (ekran chetida faqat ikonkalar).
    mini = state.get_drawer_mini()
    drawer = ui.left_drawer(fixed=True).props(f"bordered breakpoint={DRAWER_BREAKPOINT}")
    if mini:
        drawer.props("mini")

    async def toggle_drawer() -> None:
        width = await ui.run_javascript("window.innerWidth")
        if width and width >= DRAWER_BREAKPOINT:
            new_mini = not state.get_drawer_mini()
            state.set_drawer_mini(new_mini)
            if new_mini:
                drawer.props("mini")
            else:
                drawer.props(remove="mini")
        else:
            drawer.toggle()

    with ui.header().classes("items-center justify-between q-px-sm").style(f"background:{PRIMARY}"):
        with ui.row().classes("items-center gap-1 gap-sm-2"):
            ui.button(icon="menu", on_click=toggle_drawer).props("flat round dense color=white")
            ui.image("/assets/logo-mammoth.png").style("width:32px;height:32px;")
            ui.label("ShahPremium").classes("text-lg sp-brand gt-xs").style("font-size:1.1rem;")
        with ui.row().classes("items-center gap-1 gap-sm-3"):
            ui.select(
                LOCALE_LABELS,
                value=state.get_locale(),
                on_change=lambda e: _set_locale(e.value),
            ).props("dense outlined dark options-dense").style(
                "min-width:64px;background:rgba(255,255,255,.12);border-radius:8px;"
            ).tooltip("Til / Язык / Language")
            with ui.button(icon="dark_mode").props("flat round dense color=white"):
                with ui.menu():
                    ui.menu_item(t("theme.light"), on_click=lambda: _set_theme(dark_mode, "light"))
                    ui.menu_item(t("theme.dark"), on_click=lambda: _set_theme(dark_mode, "dark"))
                    ui.menu_item(t("theme.system"), on_click=lambda: _set_theme(dark_mode, "system"))
            ui.label(me.get("name") or me.get("email") or "").classes("text-sm opacity-90 gt-xs")
            ui.button(icon="logout", on_click=_logout).props("flat round dense color=white").tooltip(t("auth.logout"))

    with drawer:
        items = CLIENT_NAV_ITEMS if state.is_client() else NAV_ITEMS
        for label_key, path, icon, perm in items:
            if perm and not state.has_permission(perm):
                continue
            is_active = active == path

            # DIQQAT: bu yerda drawer.hide() CHAQIRILMAYDI — kompyuterda u panelni
            # yopib qo'yardi va yangi sahifa uni qayta ochardi (panel "yo'qolib qayta
            # chiqardi"). Yangi sahifa baribir panelni ekran kengligiga qarab chizadi.
            with ui.row().classes(
                "sp-nav-item items-center gap-3 q-pa-sm full-width cursor-pointer no-wrap "
                + ("sp-active text-primary" if is_active else "")
            ).on("click", lambda p=path: ui.navigate.to(p)):
                ui.icon(icon).classes("sp-nav-icon")
                ui.label(t(label_key)).classes("text-sm font-medium q-mini-drawer-hide ellipsis")
                if mini:
                    ui.tooltip(t(label_key)).props("anchor='center right' self='center left' :offset='[10, 0]'")

    content = ui.column().classes("w-full max-w-6xl mx-auto q-pa-sm q-pa-md-md gap-3 gap-md-4")
    return content


def _logout() -> None:
    state.clear_session()
    ui.navigate.to("/login")
