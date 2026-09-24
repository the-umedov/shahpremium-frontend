"""ShahPremium backend (FastAPI, E:\\shahpremiumuz-python) bilan ishlaydigan yupqa HTTP klient.

Bearer-token strategiyasi ishlatiladi (login javobidagi access_token saqlanadi va
har bir so'rovga Authorization header sifatida qo'shiladi) — brauzer cookie'lariga
tayanmaydi, shu bilan NiceGUI serverining o'zidan chiquvchi so'rovlar bilan mos.
"""

from __future__ import annotations

import os
from typing import Any

import httpx

BASE_URL = os.environ.get("SHAHPREMIUM_API_URL", "http://127.0.0.1:4000/api/v1")


class ApiError(Exception):
    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(message)


def _extract_error_detail(resp: httpx.Response) -> str:
    """Xato javobidan xavfsiz, qisqa xabar chiqaradi.

    MUHIM: backend uxlab qolganda (Render sleep) yoki tarmoq proksi xato bersa,
    javob bizning FastAPI JSON emas, balki Render'ning butun HTML+CSS 502
    sahifasi bo'lishi mumkin — buni to'g'ridan-to'g'ri foydalanuvchiga
    ko'rsatish (avvalgi xato) o'rniga bu yerda ushlab, qisqa tushunarli
    xabarga almashtiramiz.
    """
    content_type = resp.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            data = resp.json()
            detail = data.get("detail") or data.get("message")
            if detail:
                return str(detail)
        except Exception:
            pass
    text = resp.text.strip()
    if not text or text.startswith("<") or "html" in content_type:
        return f"Server hozircha javob bermayapti (HTTP {resp.status_code}) — birozdan so'ng qayta urinib ko'ring"
    return text[:300]


class ApiClient:
    """Har bir brauzer sessiyasi (foydalanuvchi) uchun alohida instansiya."""

    def __init__(self, access_token: str | None = None) -> None:
        self.access_token = access_token

    def _headers(self) -> dict[str, str]:
        headers = {}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    async def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=15.0) as client:
            resp = await client.request(method, path, headers=self._headers(), **kwargs)
        if resp.status_code >= 400:
            raise ApiError(resp.status_code, _extract_error_detail(resp))
        if resp.status_code == 204 or not resp.content:
            return None
        return resp.json()

    # ---- auth ----
    async def login(self, identifier: str, password: str) -> dict:
        return await self._request("POST", "/auth/login", json={"identifier": identifier, "password": password})

    async def register(
        self, *, email: str, password: str, first_name: str, last_name: str, phone: str | None = None
    ) -> dict:
        payload = {"email": email, "password": password, "first_name": first_name, "last_name": last_name}
        if phone:
            payload["phone"] = phone
        return await self._request("POST", "/auth/register", json=payload)

    async def me(self) -> dict:
        return await self._request("GET", "/auth/me")

    # ---- generic paginated list ----
    async def list_(self, resource: str, params: dict | None = None) -> dict:
        return await self._request("GET", f"/{resource}", params={k: v for k, v in (params or {}).items() if v not in (None, "")})

    async def get(self, resource: str, item_id: str) -> dict:
        return await self._request("GET", f"/{resource}/{item_id}")

    async def create(self, resource: str, payload: dict) -> dict:
        return await self._request("POST", f"/{resource}", json=payload)

    async def update(self, resource: str, item_id: str, payload: dict) -> dict:
        return await self._request("PUT", f"/{resource}/{item_id}", json=payload)

    async def delete(self, resource: str, item_id: str) -> dict:
        return await self._request("DELETE", f"/{resource}/{item_id}")

    # ---- regions: districts ----
    async def add_district(self, region_id: str, name: str) -> dict:
        return await self._request("POST", f"/regions/{region_id}/districts", json={"name": name})

    async def remove_district(self, region_id: str, district_id: str) -> dict:
        return await self._request("DELETE", f"/regions/{region_id}/districts/{district_id}")

    # ---- clients: timeline note ----
    async def add_client_note(self, client_id: str, title: str, description: str | None = None) -> dict:
        return await self._request(
            "POST", f"/clients/{client_id}/timeline", json={"title": title, "description": description}
        )

    # ---- cases: notes ----
    async def add_case_note(self, case_id: str, body: str) -> dict:
        return await self._request("POST", f"/cases/{case_id}/notes", json={"body": body})

    # ---- documents ----
    async def list_documents(self, params: dict | None = None) -> dict:
        return await self.list_("documents", params)

    async def upload_document(self, *, title: str, doc_type: str | None, case_id: str | None,
                               contract_id: str | None, client_id: str | None, access_level: str | None,
                               filename: str, content: bytes, content_type: str) -> dict:
        data = {"title": title}
        if doc_type:
            data["doc_type"] = doc_type
        if case_id:
            data["case_id"] = case_id
        if contract_id:
            data["contract_id"] = contract_id
        if client_id:
            data["client_id"] = client_id
        if access_level:
            data["access_level"] = access_level
        files = {"file": (filename, content, content_type or "application/octet-stream")}
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
            resp = await client.post("/documents", headers=self._headers(), data=data, files=files)
        if resp.status_code >= 400:
            raise ApiError(resp.status_code, _extract_error_detail(resp))
        return resp.json()

    async def document_link(self, document_id: str) -> dict:
        return await self._request("GET", f"/documents/{document_id}/link")

    # ---- employees: commission & schedule ----
    async def set_employee_commission(self, employee_id: str, commission_percent: float) -> dict:
        return await self._request(
            "PATCH", f"/employees/{employee_id}/commission", json={"commission_percent": commission_percent}
        )

    async def set_employee_schedule(self, employee_id: str, items: list[dict]) -> list[dict]:
        return await self._request("PUT", f"/employees/{employee_id}/schedule", json={"items": items})

    # ---- payments: status / refund / summary ----
    async def update_payment_status(self, payment_id: str, status: str) -> dict:
        return await self._request("PATCH", f"/payments/{payment_id}/status", json={"status": status})

    async def refund_payment(self, payment_id: str) -> dict:
        return await self._request("POST", f"/payments/{payment_id}/refund")

    async def payments_summary(self, params: dict | None = None) -> dict:
        return await self._request(
            "GET", "/payments/summary", params={k: v for k, v in (params or {}).items() if v not in (None, "")}
        )

    # ---- reports: on-screen JSON + file export ----
    async def get_report(self, report_type: str, params: dict | None = None) -> dict:
        return await self._request(
            "GET", f"/reports/{report_type}", params={k: v for k, v in (params or {}).items() if v not in (None, "")}
        )

    async def export_report(self, report_type: str, fmt: str, params: dict | None = None) -> tuple[bytes, str]:
        query = {k: v for k, v in (params or {}).items() if v not in (None, "")}
        query["format"] = fmt
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
            resp = await client.get(f"/reports/{report_type}/export", headers=self._headers(), params=query)
        if resp.status_code >= 400:
            raise ApiError(resp.status_code, _extract_error_detail(resp))
        filename = f"{report_type}.{fmt}"
        content_disposition = resp.headers.get("content-disposition", "")
        if "filename=" in content_disposition:
            filename = content_disposition.split("filename=")[-1].strip('"; ')
        return resp.content, filename

    # ---- users: role assignment ----
    async def set_user_roles(self, user_id: str, role_ids: list[str]) -> dict:
        return await self._request("PUT", f"/users/{user_id}/roles", json={"role_ids": role_ids})

    # ---- appointments: booking (bespoke endpoints, not generic CRUD) ----
    async def list_specialists(
        self, kind: str | None = None, region_id: str | None = None, search: str | None = None
    ) -> list[dict]:
        params = {k: v for k, v in {"kind": kind, "region_id": region_id, "search": search}.items() if v}
        return await self._request("GET", "/appointments/specialists", params=params)

    async def get_availability(self, assignee_id: str, date: str) -> dict:
        return await self._request(
            "GET", "/appointments/availability", params={"assignee_id": assignee_id, "date": date}
        )

    async def list_appointments(self, date_from: str, date_to: str, assignee_id: str | None = None) -> list[dict]:
        params: dict[str, str] = {"from": date_from, "to": date_to}
        if assignee_id:
            params["assignee_id"] = assignee_id
        return await self._request("GET", "/appointments/calendar", params=params)

    async def book_appointment(self, payload: dict) -> dict:
        return await self._request("POST", "/appointments", json=payload)

    async def update_appointment_status(self, appointment_id: str, status: str) -> dict:
        return await self._request("PATCH", f"/appointments/{appointment_id}/status", json={"status": status})

    # ---- appointments: office queue (jismoniy navbat/talon tizimi) ----
    async def queue_board(self, date: str | None = None, assignee_id: str | None = None) -> dict:
        params = {k: v for k, v in {"date": date, "assignee_id": assignee_id}.items() if v}
        return await self._request("GET", "/appointments/queue/board", params=params)

    async def queue_join(
        self,
        *,
        assignee_id: str | None = None,
        client_id: str | None = None,
        office_id: str | None = None,
        appointment_id: str | None = None,
    ) -> dict:
        payload = {
            "assignee_id": assignee_id,
            "client_id": client_id,
            "office_id": office_id,
            "appointment_id": appointment_id,
        }
        return await self._request("POST", "/appointments/queue", json=payload)

    async def queue_update_status(self, entry_id: str, status: str) -> dict:
        return await self._request("PATCH", f"/appointments/queue/{entry_id}/status", json={"status": status})

    # ---- tasks: kanban board + move (bespoke; create/update/delete use generic CRUD) ----
    async def task_board(self, case_id: str | None = None) -> dict:
        params = {"case_id": case_id} if case_id else {}
        return await self._request("GET", "/tasks/board", params=params)

    async def move_task(self, task_id: str, status: str) -> dict:
        return await self._request("PATCH", f"/tasks/{task_id}/move", json={"status": status})

    # ---- notifications ----
    async def list_notifications(self, params: dict | None = None) -> dict:
        return await self.list_("notifications", params)

    async def notifications_unread_count(self) -> dict:
        return await self._request("GET", "/notifications/unread-count")

    async def notifications_read_all(self) -> dict:
        return await self._request("POST", "/notifications/read-all")

    async def notifications_read_one(self, notification_id: str) -> dict:
        return await self._request("POST", f"/notifications/{notification_id}/read")

    # ---- chat (REST; realtime socket.io layer not wired up client-side) ----
    async def list_chats(self) -> list:
        return await self._request("GET", "/chat")

    async def chat_search(self, q: str) -> list:
        return await self._request("GET", "/chat/search", params={"q": q})

    async def create_chat(self, payload: dict) -> dict:
        return await self._request("POST", "/chat", json=payload)

    async def chat_messages(self, chat_id: str) -> list:
        return await self._request("GET", f"/chat/{chat_id}/messages")

    async def send_chat_message(
        self,
        chat_id: str,
        body: str,
        *,
        filename: str | None = None,
        content: bytes | None = None,
        content_type: str | None = None,
    ) -> dict:
        data = {"body": body}
        files = None
        if content is not None:
            files = {"file": (filename or "file", content, content_type or "application/octet-stream")}
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=15.0) as client:
            resp = await client.post(f"/chat/{chat_id}/messages", headers=self._headers(), data=data, files=files)
        if resp.status_code >= 400:
            raise ApiError(resp.status_code, _extract_error_detail(resp))
        return resp.json()

    async def chat_mark_read(self, chat_id: str) -> dict:
        return await self._request("POST", f"/chat/{chat_id}/read")

    # ---- audit (read-only) ----
    async def list_audit_logs(self, params: dict | None = None) -> dict:
        return await self.list_("audit", params)

    # ---- integrations ----
    async def integrations_catalog(self) -> list:
        return await self._request("GET", "/integrations/catalog")

    async def list_integrations(self) -> list:
        return await self._request("GET", "/integrations")

    async def upsert_integration(self, payload: dict) -> dict:
        return await self._request("PUT", "/integrations", json=payload)

    async def list_partners(self) -> list:
        return await self._request("GET", "/integrations/partners")

    async def create_partner(self, payload: dict) -> dict:
        return await self._request("POST", "/integrations/partners", json=payload)

    async def update_partner(self, partner_id: str, payload: dict) -> dict:
        return await self._request("PUT", f"/integrations/partners/{partner_id}", json=payload)

    async def delete_partner(self, partner_id: str) -> dict:
        return await self._request("DELETE", f"/integrations/partners/{partner_id}")

    # ---- settings: global key/value + per-user preferences ----
    async def list_settings_kv(self) -> list:
        return await self._request("GET", "/settings")

    async def upsert_setting(self, payload: dict) -> dict:
        return await self._request("PUT", "/settings", json=payload)

    async def get_preferences(self) -> dict:
        return await self._request("GET", "/settings/preferences")

    async def update_preferences(self, payload: dict) -> dict:
        return await self._request("PUT", "/settings/preferences", json=payload)
