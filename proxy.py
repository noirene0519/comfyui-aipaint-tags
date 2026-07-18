"""ComfyUI 後端代理路由：把側欄面板的請求伺服器端轉呼線上 AIPaintWorks API。

為何要代理（不讓前端直打）：ComfyUI 側欄 JS 跑在瀏覽器，直接 fetch 線上 API ＝跨域，
線上服務未開 CORS 會被瀏覽器擋。改由 ComfyUI 後端（aiohttp）伺服器端轉呼＝同源、無 CORS、
端點不外露。日配額按呼叫端 IP 計——代理的對外 IP 即使用者本機公網 IP，配額語義不變。

路由前綴 /aipaint_tags/* 為唯一撞名防線（ComfyUI 無強制命名空間）。
"""

import os
import tomllib
from pathlib import Path

import aiohttp
from aiohttp import web
from server import PromptServer

# 本節點的 Registry API（查最新發布版，供面板更新提示）
REGISTRY_API = "https://api.comfy.org"


def _local_meta() -> tuple[str, str]:
    """讀本地 pyproject.toml 的 [project] name/version（更新提示比對用）。"""
    try:
        data = tomllib.loads((Path(__file__).parent / "pyproject.toml").read_text(encoding="utf-8"))
        proj = data.get("project", {})
        return proj.get("name", ""), proj.get("version", "")
    except Exception:
        return "", ""

# 線上 API 端點（域名 aipaintworks.com 已上線 HTTPS，2026-07-17）。
# 使用者可自架服務並以環境變數 AIPAINT_API_BASE 覆寫（線上站日配額 50/IP）。
DEFAULT_API_BASE = "https://aipaintworks.com"
API_BASE = os.environ.get("AIPAINT_API_BASE", DEFAULT_API_BASE).rstrip("/")

# 冷長句經方案 E（API 編碼）可達數秒；冷啟動 503 由前端重試提示，不在此久等。
_TIMEOUT = aiohttp.ClientTimeout(total=30)

_session: aiohttp.ClientSession | None = None


async def _get_session() -> aiohttp.ClientSession:
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession(timeout=_TIMEOUT)
    return _session


async def _forward_post(path: str, payload: dict) -> web.Response:
    """轉呼上游 POST，原樣回傳 JSON 與狀態碼（含 429/503 讓前端據以提示）。"""
    session = await _get_session()
    try:
        async with session.post(f"{API_BASE}{path}", json=payload) as resp:
            body = await resp.read()
            return web.Response(
                body=body,
                status=resp.status,
                content_type="application/json",
            )
    except aiohttp.ClientError as e:
        return web.json_response({"detail": f"無法連線線上服務：{e}"}, status=502)


async def _forward_get(path: str) -> web.Response:
    session = await _get_session()
    try:
        async with session.get(f"{API_BASE}{path}") as resp:
            body = await resp.read()
            return web.Response(body=body, status=resp.status, content_type="application/json")
    except aiohttp.ClientError as e:
        return web.json_response({"detail": f"無法連線線上服務：{e}"}, status=502)


routes = PromptServer.instance.routes


@routes.post("/aipaint_tags/search")
async def aipaint_search(request: web.Request) -> web.Response:
    return await _forward_post("/search", await request.json())


@routes.post("/aipaint_tags/related")
async def aipaint_related(request: web.Request) -> web.Response:
    return await _forward_post("/related", await request.json())


@routes.get("/aipaint_tags/quota")
async def aipaint_quota(request: web.Request) -> web.Response:
    return await _forward_get("/quota")


@routes.get("/aipaint_tags/health")
async def aipaint_health(request: web.Request) -> web.Response:
    return await _forward_get("/health")


@routes.get("/aipaint_tags/version")
async def aipaint_version(request: web.Request) -> web.Response:
    """回本地版號與 Registry 最新發布版號（面板比對顯更新提示）。
    未上架/查不到時 latest=None，面板不提示。"""
    node_id, local = _local_meta()
    latest = None
    if node_id:
        session = await _get_session()
        try:
            async with session.get(f"{REGISTRY_API}/nodes/{node_id}") as resp:
                if resp.status == 200:
                    latest = ((await resp.json()).get("latest_version") or {}).get("version")
        except aiohttp.ClientError:
            pass
    return web.json_response({"local": local, "latest": latest})
