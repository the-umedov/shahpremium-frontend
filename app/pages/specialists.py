"""Mijozlar uchun: faol advokat va yuristlar ro'yxati (uchrashuvga yozilishdan oldin tanlash)."""

from __future__ import annotations

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

register(
    {
        "uz": {
            "specialists.kind.LAWYER": "Yurist",
            "specialists.kind.ADVOCATE": "Advokat",
            "specialists.filter.all": "Barchasi",
            "specialists.search": "Ism bo'yicha qidirish",
            "specialists.experience": "{n} yil tajriba",
            "specialists.book": "Uchrashuvga yozilish",
            "specialists.empty": "Hozircha faol advokat yoki yurist yo'q",
            "specialists.intro": "Ishingizni kim olib borishini tanlang va uchrashuvga yoziling.",
        },
        "ru": {
            "specialists.kind.LAWYER": "Юрист",
            "specialists.kind.ADVOCATE": "Адвокат",
            "specialists.filter.all": "Все",
            "specialists.search": "Поиск по имени",
            "specialists.experience": "Опыт {n} лет",
            "specialists.book": "Записаться на встречу",
            "specialists.empty": "Пока нет активных адвокатов или юристов",
            "specialists.intro": "Выберите специалиста и запишитесь на встречу.",
        },
        "en": {
            "specialists.kind.LAWYER": "Lawyer",
            "specialists.kind.ADVOCATE": "Advocate",
            "specialists.filter.all": "All",
            "specialists.search": "Search by name",
            "specialists.experience": "{n} years of experience",
            "specialists.book": "Book an appointment",
            "specialists.empty": "No active advocates or lawyers yet",
            "specialists.intro": "Choose who will handle your case and book an appointment.",
        },
    }
)


def _full_name(spec: dict) -> str:
    profile = ((spec.get("user") or {}).get("profile")) or {}
    return f"{profile.get('first_name', '')} {profile.get('last_name', '')}".strip() or "—"


def render_specialist_cards(items: list[dict]) -> None:
    """Kartalar to'ri — shu sahifada ham, mijoz boshqaruv panelida ham ishlatiladi."""
    if not items:
        ui.label(t("specialists.empty")).classes("sp-subtle")
        return
    with ui.grid().classes("w-full gap-3 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3"):
        for spec in items:
            kind = spec.get("kind") or ""
            region = ((spec.get("user") or {}).get("region") or {}).get("name")
            with ui.card().classes("sp-card q-pa-md w-full gap-1"):
                with ui.row().classes("w-full items-center justify-between no-wrap"):
                    with ui.row().classes("items-center gap-2 no-wrap"):
                        ui.icon("account_circle").classes("text-4xl text-primary")
                        ui.label(_full_name(spec)).classes("text-base font-bold")
                    ui.badge(t(f"specialists.kind.{kind}")).props(
                        f"color={'primary' if kind == 'ADVOCATE' else 'secondary'}"
                    )
                if spec.get("specialization"):
                    ui.label(spec["specialization"]).classes("sp-text-2 text-sm")
                meta = []
                if spec.get("experience_years"):
                    meta.append(t("specialists.experience").format(n=spec["experience_years"]))
                if region:
                    meta.append(region)
                if meta:
                    ui.label(" · ".join(meta)).classes("sp-muted text-caption")
                ui.button(t("specialists.book"), icon="event", on_click=lambda: ui.navigate.to("/appointments")).props(
                    "flat dense color=primary"
                ).classes("q-mt-xs")


def render() -> None:
    if not require_login():
        return

    with shell(active="/specialists"):
        ui.label(t("nav.specialists")).classes("text-2xl font-bold")
        ui.label(t("specialists.intro")).classes("sp-text-2")

        with ui.row().classes("w-full items-center gap-2"):
            kind = ui.select(
                {"": t("specialists.filter.all"), "ADVOCATE": t("specialists.kind.ADVOCATE"), "LAWYER": t("specialists.kind.LAWYER")},
                value="",
            ).props("outlined dense").classes("col-12 col-sm-3")
            search = ui.input(t("specialists.search")).props("outlined dense clearable").classes("col")

        container = ui.column().classes("w-full")

        async def reload() -> None:
            try:
                items = await state.client().list_specialists(kind=kind.value or None, search=search.value or None)
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            container.clear()
            with container:
                render_specialist_cards(items or [])

        kind.on_value_change(reload)
        search.on("keydown.enter", reload)
        search.on("clear", reload)
        ui.timer(0.05, reload, once=True)
