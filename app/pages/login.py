from __future__ import annotations

from nicegui import ui

from app import state
from app.api_client import ApiClient, ApiError
from app.i18n import LOCALE_LABELS, register, t
from app.theme import BRAND_OVERRIDE_CSS, GOLD_DEEP

register(
    {
        "uz": {
            "login.subtitle": "Yuridik SaaS platforma",
            "login.required": "Login va parolni kiriting",
            "login.network_error": "Serverga ulanib bo'lmadi",
            "login.copyright": "© ShahPremium",
            "login.tab_login": "Kirish",
            "login.tab_register": "Ro'yxatdan o'tish",
            "register.first_name": "Ism",
            "register.last_name": "Familiya",
            "register.email": "Email",
            "register.phone": "Telefon (ixtiyoriy)",
            "register.password": "Parol",
            "register.confirm_password": "Parolni tasdiqlang",
            "register.submit": "Ro'yxatdan o'tish",
            "register.required": "Ism, familiya, email va parolni kiriting",
            "register.password_mismatch": "Parollar mos kelmadi",
            "register.password_weak": "Parol kamida 8 belgi, harf va raqamdan iborat bo'lsin",
            "register.success": "Ro'yxatdan muvaffaqiyatli o'tdingiz — tizimga kirilyapti...",
        },
        "ru": {
            "login.subtitle": "Юридическая SaaS-платформа",
            "login.required": "Введите логин и пароль",
            "login.network_error": "Не удалось подключиться к серверу",
            "login.copyright": "© ShahPremium",
            "login.tab_login": "Вход",
            "login.tab_register": "Регистрация",
            "register.first_name": "Имя",
            "register.last_name": "Фамилия",
            "register.email": "Email",
            "register.phone": "Телефон (необязательно)",
            "register.password": "Пароль",
            "register.confirm_password": "Подтвердите пароль",
            "register.submit": "Зарегистрироваться",
            "register.required": "Введите имя, фамилию, email и пароль",
            "register.password_mismatch": "Пароли не совпадают",
            "register.password_weak": "Пароль минимум 8 символов, с буквой и цифрой",
            "register.success": "Регистрация прошла успешно — выполняется вход...",
        },
        "en": {
            "login.subtitle": "Legal SaaS platform",
            "login.required": "Enter your login and password",
            "login.network_error": "Could not connect to the server",
            "login.copyright": "© ShahPremium",
            "login.tab_login": "Log in",
            "login.tab_register": "Register",
            "register.first_name": "First name",
            "register.last_name": "Last name",
            "register.email": "Email",
            "register.phone": "Phone (optional)",
            "register.password": "Password",
            "register.confirm_password": "Confirm password",
            "register.submit": "Register",
            "register.required": "Enter first name, last name, email and password",
            "register.password_mismatch": "Passwords do not match",
            "register.password_weak": "Password must be at least 8 characters with a letter and a digit",
            "register.success": "Registered successfully — signing you in...",
        },
    }
)


async def _finish_login(identifier: str, password: str, error_label: ui.label) -> None:
    api = ApiClient()
    try:
        tokens = await api.login(identifier, password)
        api.access_token = tokens["access_token"]
        me = await api.me()
        state.set_session(access_token=tokens["access_token"], me=me)
        ui.navigate.to("/")
    except ApiError as exc:
        error_label.text = exc.message
    except Exception as exc:  # noqa: BLE001 — tarmoq xatosi, backend ishlamayotgan bo'lishi mumkin
        error_label.text = f"{t('login.network_error')}: {exc}"


def render() -> None:
    ui.add_head_html(BRAND_OVERRIDE_CSS)
    dark_mode = ui.dark_mode()
    theme = state.get_theme()
    dark_mode.value = True if theme == "dark" else (False if theme == "light" else None)

    with ui.row().classes("absolute top-0 right-0 q-ma-md gap-2 z-top"):
        ui.select(
            LOCALE_LABELS,
            value=state.get_locale(),
            on_change=lambda e: (state.set_locale(e.value), ui.navigate.reload()),
        ).props("dense outlined options-dense").style("min-width:110px;")

    with ui.column().classes("absolute-center items-center gap-1"):
        ui.image("/assets/logo-mammoth.png").style("width:110px;height:110px;")
        ui.label("SHAH PREMIUM").classes("sp-brand text-xl q-mt-xs").style(f"color:{GOLD_DEEP};")
        ui.label(t("login.subtitle")).classes("text-sm text-grey-6 q-mb-md")

        with ui.card().classes("sp-card q-pa-lg").style("width:380px; border-radius:16px;"):
            with ui.tabs().classes("w-full") as auth_tabs:
                login_tab = ui.tab(t("login.tab_login"))
                register_tab = ui.tab(t("login.tab_register"))
            with ui.tab_panels(auth_tabs, value=login_tab).classes("w-full"):
                with ui.tab_panel(login_tab).classes("q-pa-none q-pt-md"):
                    _login_panel()
                with ui.tab_panel(register_tab).classes("q-pa-none q-pt-md"):
                    _register_panel()

        ui.label(t("login.copyright")).classes("text-caption text-grey-5 q-mt-md")


def _login_panel() -> None:
    identifier = ui.input(t("auth.identifier")).props("outlined dense").classes("w-full")
    password = ui.input(t("auth.password"), password=True, password_toggle_button=True).props(
        "outlined dense"
    ).classes("w-full q-mt-sm")
    otp = ui.input(t("auth.otp")).props("outlined dense").classes("w-full q-mt-sm")
    error_label = ui.label("").classes("text-red-6 text-caption")

    async def do_login() -> None:
        error_label.text = ""
        if not identifier.value or not password.value:
            error_label.text = t("login.required")
            return
        await _finish_login(identifier.value, password.value, error_label)

    ui.button(t("auth.submit"), on_click=do_login).props("unelevated color=indigo-7").classes("w-full q-mt-md")
    password.on("keydown.enter", do_login)
    otp.on("keydown.enter", do_login)


def _register_panel() -> None:
    first_name = ui.input(t("register.first_name")).props("outlined dense").classes("w-full")
    last_name = ui.input(t("register.last_name")).props("outlined dense").classes("w-full q-mt-sm")
    email = ui.input(t("register.email")).props("outlined dense").classes("w-full q-mt-sm")
    phone = ui.input(t("register.phone")).props("outlined dense").classes("w-full q-mt-sm")
    password = ui.input(t("register.password"), password=True, password_toggle_button=True).props(
        "outlined dense"
    ).classes("w-full q-mt-sm")
    confirm = ui.input(t("register.confirm_password"), password=True, password_toggle_button=True).props(
        "outlined dense"
    ).classes("w-full q-mt-sm")
    error_label = ui.label("").classes("text-red-6 text-caption")

    async def do_register() -> None:
        error_label.text = ""
        if not first_name.value or not last_name.value or not email.value or not password.value:
            error_label.text = t("register.required")
            return
        if password.value != confirm.value:
            error_label.text = t("register.password_mismatch")
            return
        if len(password.value) < 8 or password.value.isalpha() or password.value.isdigit():
            error_label.text = t("register.password_weak")
            return
        api = ApiClient()
        try:
            await api.register(
                email=email.value,
                password=password.value,
                first_name=first_name.value,
                last_name=last_name.value,
                phone=phone.value or None,
            )
        except ApiError as exc:
            error_label.text = exc.message
            return
        except Exception as exc:  # noqa: BLE001
            error_label.text = f"{t('login.network_error')}: {exc}"
            return
        ui.notify(t("register.success"), type="positive")
        # Ro'yxatdan o'tish token qaytarmaydi (email tasdiqlash oqimi bor) —
        # qulaylik uchun darhol shu login/parol bilan kirishga urinamiz.
        await _finish_login(email.value, password.value, error_label)

    ui.button(t("register.submit"), on_click=do_register).props("unelevated color=indigo-7").classes("w-full q-mt-md")
    confirm.on("keydown.enter", do_register)
