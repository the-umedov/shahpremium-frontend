from __future__ import annotations

from nicegui import ui

from app import state
from app.api_client import ApiError
from app.i18n import register, t
from app.shell import require_login, shell

ACCESS_LEVELS = ["PRIVATE", "OFFICE", "CLIENT_SHARED", "RESTRICTED"]

register(
    {
        "uz": {
            "documents.upload": "Hujjat yuklash",
            "documents.search_placeholder": "Qidirish (sarlavha)",
            "documents.col_title": "Sarlavha",
            "documents.col_doc_type": "Turi",
            "documents.col_access_level": "Ruxsat darajasi",
            "documents.col_version": "Versiya",
            "documents.col_mime": "Format",
            "documents.total_line": "Jami: {n} ta",
            "documents.title_input": "Sarlavha *",
            "documents.doc_type_input": "Hujjat turi",
            "documents.case_id_input": "Ish ID (ixtiyoriy)",
            "documents.client_id_input": "Mijoz ID (ixtiyoriy)",
            "documents.picked": "Tanlandi: {name}",
            "documents.upload_label": "Fayl tanlang (PDF/DOCX/XLSX/JPG/PNG, 25MB gacha)",
            "documents.title_file_required": "Sarlavha va fayl majburiy",
            "documents.uploaded": "Hujjat yuklandi",
            "documents.type_access_line": "Turi: {doc_type} · Ruxsat: {access_level}",
            "documents.version_mime_line": "Joriy versiya: {version} · Format: {mime}",
            "documents.versions_title": "Versiyalar tarixi ({n})",
            "documents.download_link": "Yuklab olish havolasi",
            "documents.link_line": "Havola: {url}",
            "documents.deleted": "Hujjat o'chirildi",
            "status.PRIVATE": "Shaxsiy",
            "status.OFFICE": "Ofis",
            "status.CLIENT_SHARED": "Mijoz bilan bo'lishilgan",
            "status.RESTRICTED": "Cheklangan",
        },
        "ru": {
            "documents.upload": "Загрузить документ",
            "documents.search_placeholder": "Поиск (заголовок)",
            "documents.col_title": "Заголовок",
            "documents.col_doc_type": "Тип",
            "documents.col_access_level": "Уровень доступа",
            "documents.col_version": "Версия",
            "documents.col_mime": "Формат",
            "documents.total_line": "Всего: {n}",
            "documents.title_input": "Заголовок *",
            "documents.doc_type_input": "Тип документа",
            "documents.case_id_input": "ID дела (необязательно)",
            "documents.client_id_input": "ID клиента (необязательно)",
            "documents.picked": "Выбрано: {name}",
            "documents.upload_label": "Выберите файл (PDF/DOCX/XLSX/JPG/PNG, до 25MB)",
            "documents.title_file_required": "Заголовок и файл обязательны",
            "documents.uploaded": "Документ загружен",
            "documents.type_access_line": "Тип: {doc_type} · Доступ: {access_level}",
            "documents.version_mime_line": "Текущая версия: {version} · Формат: {mime}",
            "documents.versions_title": "История версий ({n})",
            "documents.download_link": "Ссылка для скачивания",
            "documents.link_line": "Ссылка: {url}",
            "documents.deleted": "Документ удалён",
            "status.PRIVATE": "Приватный",
            "status.OFFICE": "Офис",
            "status.CLIENT_SHARED": "Доступен клиенту",
            "status.RESTRICTED": "Ограниченный",
        },
        "en": {
            "documents.upload": "Upload document",
            "documents.search_placeholder": "Search (title)",
            "documents.col_title": "Title",
            "documents.col_doc_type": "Type",
            "documents.col_access_level": "Access level",
            "documents.col_version": "Version",
            "documents.col_mime": "Format",
            "documents.total_line": "Total: {n}",
            "documents.title_input": "Title *",
            "documents.doc_type_input": "Document type",
            "documents.case_id_input": "Case ID (optional)",
            "documents.client_id_input": "Client ID (optional)",
            "documents.picked": "Selected: {name}",
            "documents.upload_label": "Choose a file (PDF/DOCX/XLSX/JPG/PNG, up to 25MB)",
            "documents.title_file_required": "Title and file are required",
            "documents.uploaded": "Document uploaded",
            "documents.type_access_line": "Type: {doc_type} · Access: {access_level}",
            "documents.version_mime_line": "Current version: {version} · Format: {mime}",
            "documents.versions_title": "Version history ({n})",
            "documents.download_link": "Download link",
            "documents.link_line": "Link: {url}",
            "documents.deleted": "Document deleted",
            "status.PRIVATE": "Private",
            "status.OFFICE": "Office",
            "status.CLIENT_SHARED": "Shared with client",
            "status.RESTRICTED": "Restricted",
        },
    }
)


def _status_label(value: str) -> str:
    key = f"status.{value}"
    label = t(key)
    return value if label == key else label


def render() -> None:
    if not require_login():
        return

    columns = [
        {"name": "title", "label": t("documents.col_title"), "field": "title", "align": "left"},
        {"name": "doc_type", "label": t("documents.col_doc_type"), "field": "doc_type", "align": "left"},
        {"name": "access_level", "label": t("documents.col_access_level"), "field": "access_level", "align": "left"},
        {"name": "current_version", "label": t("documents.col_version"), "field": "current_version", "align": "left"},
        {"name": "mime_type", "label": t("documents.col_mime"), "field": "mime_type", "align": "left"},
    ]

    with shell(active="/documents"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label(t("nav.documents")).classes("text-2xl font-bold")
            btn = ui.button(t("documents.upload"), icon="upload", on_click=lambda: _open_upload_dialog(reload))
            btn.props("unelevated color=indigo-7")
            btn.set_visibility(state.has_permission("documents.upload"))

        search = ui.input(t("documents.search_placeholder")).props("outlined dense clearable").classes("w-full")
        table = ui.table(columns=columns, rows=[], row_key="id").classes("w-full sp-card").props("flat bordered")
        table.on("rowClick", lambda e: _open_detail_dialog(e.args[1]["id"], reload))
        info_row = ui.row().classes("items-center justify-between w-full")

        async def reload() -> None:
            try:
                result = await state.client().list_documents({"page": 1, "limit": 50, "search": search.value})
            except ApiError as exc:
                ui.notify(exc.message, type="negative")
                return
            table.rows = result.get("items", [])
            info_row.clear()
            with info_row:
                ui.label(t("documents.total_line").format(n=result.get("meta", {}).get("total", 0)))

        search.on("keydown.enter", reload)
        ui.timer(0.05, reload, once=True)


def _open_upload_dialog(on_saved) -> None:
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:420px;"):
        ui.label(t("documents.upload")).classes("text-lg font-bold")
        title = ui.input(t("documents.title_input")).props("outlined dense").classes("w-full")
        doc_type = ui.input(t("documents.doc_type_input")).props("outlined dense").classes("w-full")
        case_id = ui.input(t("documents.case_id_input")).props("outlined dense").classes("w-full")
        client_id = ui.input(t("documents.client_id_input")).props("outlined dense").classes("w-full")
        access_level = ui.select(ACCESS_LEVELS, value="OFFICE", label=t("documents.col_access_level")).props("outlined dense").classes("w-full")
        err = ui.label("").classes("text-red-6 text-caption")
        picked = {"content": None, "name": None, "type": None}

        def on_upload(e) -> None:
            picked["content"] = e.content.read()
            picked["name"] = e.name
            picked["type"] = e.type
            ui.notify(t("documents.picked").format(name=e.name), type="info")

        ui.upload(on_upload=on_upload, auto_upload=True, max_files=1).props(
            f'label="{t("documents.upload_label")}"'
        ).classes("w-full")

        async def save() -> None:
            if not title.value or not picked["content"]:
                err.text = t("documents.title_file_required")
                return
            try:
                await state.client().upload_document(
                    title=title.value,
                    doc_type=doc_type.value or None,
                    case_id=case_id.value or None,
                    contract_id=None,
                    client_id=client_id.value or None,
                    access_level=access_level.value,
                    filename=picked["name"],
                    content=picked["content"],
                    content_type=picked["type"],
                )
            except ApiError as exc:
                err.text = exc.message
                return
            ui.notify(t("documents.uploaded"), type="positive")
            dialog.close()
            await on_saved()

        with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
            ui.button(t("common.cancel"), on_click=dialog.close).props("flat")
            ui.button(t("common.save"), on_click=save).props("unelevated color=indigo-7")
    dialog.open()


def _open_detail_dialog(document_id: str, on_changed) -> None:
    with ui.dialog() as dialog, ui.card().classes("q-pa-md").style("min-width:480px; max-width:640px;"):
        content = ui.column().classes("w-full gap-2")
        with content:
            ui.spinner()

        async def load() -> None:
            try:
                data = await state.client().get("documents", document_id)
            except ApiError as exc:
                content.clear()
                with content:
                    ui.label(exc.message).classes("text-red-6")
                return
            content.clear()
            with content:
                ui.label(data.get("title", "")).classes("text-xl font-bold")
                ui.label(
                    t("documents.type_access_line").format(
                        doc_type=data.get("doc_type") or "—",
                        access_level=_status_label(data.get("access_level") or ""),
                    )
                )
                ui.label(
                    t("documents.version_mime_line").format(
                        version=data.get("current_version"), mime=data.get("mime_type") or "—"
                    )
                )

                versions = data.get("versions") or []
                ui.separator().classes("q-my-sm")
                ui.label(t("documents.versions_title").format(n=len(versions))).classes("text-md font-semibold")
                for v in versions[:10]:
                    ui.label(f"v{v.get('version')} — {v.get('comment') or ''}").classes("text-sm")

                async def get_link() -> None:
                    try:
                        link = await state.client().document_link(document_id)
                    except ApiError as exc:
                        ui.notify(exc.message, type="negative")
                        return
                    ui.notify(t("documents.link_line").format(url=link.get("url")), type="info", timeout=10000)

                with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
                    ui.button(t("documents.download_link"), icon="link", on_click=get_link).props("flat color=indigo-7")
                    if state.has_permission("documents.delete"):
                        async def remove() -> None:
                            try:
                                await state.client().delete("documents", document_id)
                            except ApiError as exc:
                                ui.notify(exc.message, type="negative")
                                return
                            ui.notify(t("documents.deleted"), type="positive")
                            dialog.close()
                            await on_changed()

                        ui.button(t("common.delete"), on_click=remove).props("flat color=red")
                    ui.button(t("common.close"), on_click=dialog.close).props("flat")

        ui.timer(0.05, load, once=True)
    dialog.open()
