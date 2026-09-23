"""i18n: ru / uz / en — 04_Design_System_i18n.md talabiga ko'ra.

Foydalanish:
    from app.i18n import t, register
    register({
        "uz": {"employees.title": "Xodimlar"},
        "ru": {"employees.title": "Сотрудники"},
        "en": {"employees.title": "Employees"},
    })
    ...
    ui.label(t("employees.title"))

Har bir sahifa modul darajasida FAQAT O'ZINING kalitlarini `register()` qiladi —
bu boshqa modullar bilan bir xil faylni bir vaqtda tahrirlash (merge conflict)
xavfini yo'q qiladi. Umumiy (common/nav/auth/dashboard) kalitlar shu faylning
o'zida DEFAULT sifatida beriladi.
"""

from __future__ import annotations

CATALOG: dict[str, dict[str, str]] = {
    "uz": {
        "common.save": "Saqlash",
        "common.cancel": "Bekor qilish",
        "common.create": "Yaratish",
        "common.edit": "Tahrirlash",
        "common.delete": "O'chirish",
        "common.search": "Qidirish",
        "common.loading": "Yuklanmoqda...",
        "common.no_data": "Ma'lumot yo'q",
        "common.error": "Xatolik yuz berdi",
        "common.confirm_delete": "Haqiqatan ham o'chirmoqchimisiz?",
        "common.actions": "Amallar",
        "common.status": "Holat",
        "common.name": "Nomi",
        "common.close": "Yopish",
        "common.yes": "Ha",
        "common.no": "Yo'q",
        "common.total": "Jami",
        "nav.dashboard": "Boshqaruv paneli",
        "nav.clients": "Mijozlar",
        "nav.cases": "Ishlar",
        "nav.contracts": "Shartnomalar",
        "nav.documents": "Hujjatlar",
        "nav.appointments": "Uchrashuvlar",
        "nav.tasks": "Vazifalar",
        "nav.payments": "To'lovlar",
        "nav.reports": "Hisobotlar",
        "nav.notifications": "Bildirishnomalar",
        "nav.chat": "Suhbatlar",
        "nav.employees": "Xodimlar",
        "nav.regions": "Viloyatlar",
        "nav.offices": "Ofislar",
        "nav.services": "Xizmatlar",
        "nav.users": "Foydalanuvchilar",
        "nav.roles": "Rollar",
        "nav.permissions": "Ruxsatlar",
        "nav.audit": "Audit jurnali",
        "nav.integrations": "Integratsiyalar",
        "nav.settings": "Sozlamalar",
        "auth.login_title": "Kirish",
        "auth.identifier": "Email yoki telefon",
        "auth.password": "Parol",
        "auth.submit": "Kirish",
        "auth.logout": "Chiqish",
        "auth.otp": "2FA kodi (agar yoqilgan bo'lsa)",
        "theme.light": "Yorug'",
        "theme.dark": "Qorong'i",
        "theme.system": "Tizim",
    },
    "ru": {
        "common.save": "Сохранить",
        "common.cancel": "Отмена",
        "common.create": "Создать",
        "common.edit": "Редактировать",
        "common.delete": "Удалить",
        "common.search": "Поиск",
        "common.loading": "Загрузка...",
        "common.no_data": "Нет данных",
        "common.error": "Произошла ошибка",
        "common.confirm_delete": "Вы уверены, что хотите удалить это?",
        "common.actions": "Действия",
        "common.status": "Статус",
        "common.name": "Название",
        "common.close": "Закрыть",
        "common.yes": "Да",
        "common.no": "Нет",
        "common.total": "Всего",
        "nav.dashboard": "Дашборд",
        "nav.clients": "Клиенты",
        "nav.cases": "Дела",
        "nav.contracts": "Договоры",
        "nav.documents": "Документы",
        "nav.appointments": "Записи",
        "nav.tasks": "Задачи",
        "nav.payments": "Платежи",
        "nav.reports": "Отчёты",
        "nav.notifications": "Уведомления",
        "nav.chat": "Чат",
        "nav.employees": "Сотрудники",
        "nav.regions": "Регионы",
        "nav.offices": "Офисы",
        "nav.services": "Услуги",
        "nav.users": "Пользователи",
        "nav.roles": "Роли",
        "nav.permissions": "Права доступа",
        "nav.audit": "Журнал аудита",
        "nav.integrations": "Интеграции",
        "nav.settings": "Настройки",
        "auth.login_title": "Вход",
        "auth.identifier": "Email или телефон",
        "auth.password": "Пароль",
        "auth.submit": "Войти",
        "auth.logout": "Выйти",
        "auth.otp": "Код 2FA (если включён)",
        "theme.light": "Светлая",
        "theme.dark": "Тёмная",
        "theme.system": "Системная",
    },
    "en": {
        "common.save": "Save",
        "common.cancel": "Cancel",
        "common.create": "Create",
        "common.edit": "Edit",
        "common.delete": "Delete",
        "common.search": "Search",
        "common.loading": "Loading...",
        "common.no_data": "No data",
        "common.error": "Something went wrong",
        "common.confirm_delete": "Are you sure you want to delete this?",
        "common.actions": "Actions",
        "common.status": "Status",
        "common.name": "Name",
        "common.close": "Close",
        "common.yes": "Yes",
        "common.no": "No",
        "common.total": "Total",
        "nav.dashboard": "Dashboard",
        "nav.clients": "Clients",
        "nav.cases": "Cases",
        "nav.contracts": "Contracts",
        "nav.documents": "Documents",
        "nav.appointments": "Appointments",
        "nav.tasks": "Tasks",
        "nav.payments": "Payments",
        "nav.reports": "Reports",
        "nav.notifications": "Notifications",
        "nav.chat": "Chat",
        "nav.employees": "Employees",
        "nav.regions": "Regions",
        "nav.offices": "Offices",
        "nav.services": "Services",
        "nav.users": "Users",
        "nav.roles": "Roles",
        "nav.permissions": "Permissions",
        "nav.audit": "Audit log",
        "nav.integrations": "Integrations",
        "nav.settings": "Settings",
        "auth.login_title": "Log in",
        "auth.identifier": "Email or phone",
        "auth.password": "Password",
        "auth.submit": "Log in",
        "auth.logout": "Log out",
        "auth.otp": "2FA code (if enabled)",
        "theme.light": "Light",
        "theme.dark": "Dark",
        "theme.system": "System",
    },
}

DEFAULT_LOCALE = "uz"
SUPPORTED_LOCALES = ["uz", "ru", "en"]


def register(translations: dict[str, dict[str, str]]) -> None:
    """Modul o'z kalitlarini shu funksiya orqali qo'shadi (merge, qayta yozmaydi)."""
    for locale, entries in translations.items():
        CATALOG.setdefault(locale, {}).update(entries)


def t(key: str) -> str:
    """Joriy tildagi tarjima. `app.state.get_locale()` orqali joriy tilni oladi."""
    from app import state  # local import — aylanma import'dan qochish uchun

    locale = state.get_locale()
    value = CATALOG.get(locale, {}).get(key)
    if value is not None:
        return value
    fallback = CATALOG.get(DEFAULT_LOCALE, {}).get(key)
    return fallback if fallback is not None else key
