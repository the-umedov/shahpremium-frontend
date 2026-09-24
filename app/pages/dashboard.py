from __future__ import annotations

from decimal import Decimal, InvalidOperation

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.pages.specialists import render_specialist_cards
from app.shell import require_login, shell

register(
    {
        "uz": {
            "dashboard.welcome": "Xush kelibsiz",
            "dashboard.roles": "rollar",
            "dashboard.no_roles": "yo'q",
            "dashboard.stats": "Statistika",
            "dashboard.paid": "To'langan",
            "dashboard.pending": "Kutilmoqda",
            "dashboard.my_payments": "To'lovlarim",
            "dashboard.no_payments": "Hozircha to'lovlar yo'q",
            "dashboard.see_all": "Barchasi",
        },
        "ru": {
            "dashboard.welcome": "С возвращением",
            "dashboard.roles": "роли",
            "dashboard.no_roles": "нет",
            "dashboard.stats": "Статистика",
            "dashboard.paid": "Оплачено",
            "dashboard.pending": "Ожидается",
            "dashboard.my_payments": "Мои платежи",
            "dashboard.no_payments": "Платежей пока нет",
            "dashboard.see_all": "Все",
        },
        "en": {
            "dashboard.welcome": "Welcome back",
            "dashboard.roles": "roles",
            "dashboard.no_roles": "none",
            "dashboard.stats": "Statistics",
            "dashboard.paid": "Paid",
            "dashboard.pending": "Pending",
            "dashboard.my_payments": "My payments",
            "dashboard.no_payments": "No payments yet",
            "dashboard.see_all": "See all",
        },
    }
)


def render() -> None:
    if not require_login():
        return
    me = state.get_me() or {}

    with shell(active="/"):
        ui.label(t("nav.dashboard")).classes("text-2xl font-bold")
        roles = ", ".join(me.get("roles") or []) or t("dashboard.no_roles")
        ui.label(f"{t('dashboard.welcome')} — {t('dashboard.roles')}: {roles}").classes("sp-text-2")

        if state.is_client():
            _render_client_dashboard()
            return

        # Telefonda 2x2, planshet/kompyuterda 4 ustunli qator.
        # DIQQAT: `columns=` parametrini bermaymiz — u inline `style` sifatida
        # qo'yiladi va Tailwind'ning `md:grid-cols-4` klassidan ustun kelib,
        # responsive xatti-harakatni butunlay bloklardi.
        with ui.grid().classes("w-full gap-3 grid-cols-2 md:grid-cols-4"):
            _stat_card(t("nav.clients"), "clients", "clients.read", "groups")
            _stat_card(t("nav.cases"), "cases", "cases.read", "gavel")
            _stat_card(t("nav.contracts"), "contracts", "contracts.read", "description")
            _stat_card(t("nav.documents"), "documents", "documents.read", "folder")


def _stat_card(label: str, resource: str, perm: str, icon: str) -> None:
    card = ui.card().classes("sp-card q-pa-md w-full")
    if state.has_permission(perm):
        card.classes("sp-clickable").on("click", lambda: ui.navigate.to(f"/{resource}"))
    with card:
        ui.icon(icon).classes("text-3xl text-primary")
        ui.label(label).classes("sp-text-2 text-sm")
        value_label = ui.label("…").classes("text-2xl font-bold")

        async def load() -> None:
            if not state.has_permission(perm):
                value_label.text = "—"
                return
            try:
                page = await state.client().list_(resource, {"page": 1, "limit": 1})
                value_label.text = str(page.get("meta", {}).get("total", "—"))
            except ApiError:
                value_label.text = "—"
            except Exception:
                value_label.text = "—"

        ui.timer(0.05, load, once=True)


# ---------------------------------------------------------------------------
# Mijoz (CLIENT) boshqaruv paneli: "Mijozlar" o'rniga Statistika, to'lovlar va
# advokat/yuristlar shu yerning o'zida.
# ---------------------------------------------------------------------------


def _money(value: Decimal, currency: str = "UZS") -> str:
    return f"{value:,.0f}".replace(",", " ") + f" {currency}"


def _to_decimal(raw) -> Decimal:
    try:
        return Decimal(str(raw))
    except (InvalidOperation, TypeError):
        return Decimal(0)


def _render_client_dashboard() -> None:
    with ui.grid().classes("w-full gap-3 grid-cols-2 md:grid-cols-4"):
        stats_card = ui.card().classes("sp-card sp-clickable q-pa-md w-full").on(
            "click", lambda: ui.navigate.to("/payments")
        )
        with stats_card:
            ui.icon("insights").classes("text-3xl text-primary")
            ui.label(t("dashboard.stats")).classes("sp-text-2 text-sm")
            paid_label = ui.label("…").classes("text-base font-bold text-positive")
            pending_label = ui.label("").classes("text-caption sp-muted")
        _stat_card(t("nav.cases"), "cases", "cases.read", "gavel")
        _stat_card(t("nav.contracts"), "contracts", "contracts.read", "description")
        _stat_card(t("nav.documents"), "documents", "documents.read", "folder")

    # ---- To'lovlarim ----
    with ui.row().classes("w-full items-center justify-between q-mt-md"):
        ui.label(t("dashboard.my_payments")).classes("text-lg font-bold")
        ui.button(t("dashboard.see_all"), icon="arrow_forward", on_click=lambda: ui.navigate.to("/payments")).props(
            "flat dense color=primary"
        )
    payments_box = ui.column().classes("w-full")

    # ---- Advokat va yuristlar ----
    with ui.row().classes("w-full items-center justify-between q-mt-md"):
        ui.label(t("nav.specialists")).classes("text-lg font-bold")
        ui.button(t("dashboard.see_all"), icon="arrow_forward", on_click=lambda: ui.navigate.to("/specialists")).props(
            "flat dense color=primary"
        )
    specialists_box = ui.column().classes("w-full")

    async def load_payments() -> None:
        if not state.has_permission("payments.read"):
            paid_label.text = "—"
            return
        try:
            page = await state.client().list_("payments", {"page": 1, "limit": 100})
        except ApiError as exc:
            paid_label.text = "—"
            with payments_box:
                ui.label(exc.message).classes("text-negative")
            return
        items = page.get("items", [])
        currency = (items[0].get("currency") if items else None) or "UZS"
        paid = sum((_to_decimal(p.get("amount")) for p in items if p.get("status") == "PAID"), Decimal(0))
        pending = sum((_to_decimal(p.get("amount")) for p in items if p.get("status") == "PENDING"), Decimal(0))
        paid_label.text = f"{t('dashboard.paid')}: {_money(paid, currency)}"
        pending_label.text = f"{t('dashboard.pending')}: {_money(pending, currency)}"

        payments_box.clear()
        with payments_box:
            if not items:
                ui.label(t("dashboard.no_payments")).classes("sp-subtle")
                return
            columns = [
                {"name": "created_at", "label": "", "field": "created_at", "align": "left"},
                {"name": "category", "label": "", "field": "category", "align": "left"},
                {"name": "amount", "label": "", "field": "amount", "align": "right"},
                {"name": "status", "label": "", "field": "status", "align": "left"},
            ]
            rows = [
                {
                    "id": p["id"],
                    "created_at": str(p.get("created_at") or "")[:10],
                    "category": t(f"status.{p.get('category')}") if p.get("category") else "—",
                    "amount": _money(_to_decimal(p.get("amount")), p.get("currency") or currency),
                    "status": t(f"status.{p.get('status')}"),
                }
                for p in items[:5]
            ]
            ui.table(columns=columns, rows=rows, row_key="id").classes("w-full sp-card").props(
                "flat bordered hide-header"
            )

    async def load_specialists() -> None:
        try:
            items = await state.client().list_specialists()
        except ApiError:
            items = []
        specialists_box.clear()
        with specialists_box:
            render_specialist_cards((items or [])[:6])

    ui.timer(0.05, load_payments, once=True)
    ui.timer(0.1, load_specialists, once=True)
