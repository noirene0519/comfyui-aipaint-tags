"""AIPaintWorks 標籤語義搜尋 — ComfyUI 側欄工具（路線 A 薄客戶端）。

純前端擴充（無運算節點）：
- WEB_DIRECTORY 匯出 js/ 內的側欄面板腳本（ComfyUI 自動載入 .js）。
- proxy 模組在 ComfyUI 後端註冊 /aipaint_tags/* 路由，伺服器端代理轉呼線上
  AIPaintWorks API——前端只打 ComfyUI 同源路由，避開 CORS、隱藏端點。

線上 API 端點以環境變數 AIPAINT_API_BASE 覆寫（預設見 proxy.py）。
"""

from . import proxy  # noqa: F401  匯入即註冊 PromptServer 路由

WEB_DIRECTORY = "./js"

# 純前端擴充無運算節點；但部分 ComfyUI 版本的 loader 若模組無 NODE_CLASS_MAPPINGS
# 會印「Skip … IMPORT FAILED」警告（WEB_DIRECTORY 其實已註冊、功能不受影響）。
# 給空 dict 讓 loader 判定成功、靜音警告（loader 只檢查 is not None，非真值）。
NODE_CLASS_MAPPINGS: dict = {}

__all__ = ["WEB_DIRECTORY", "NODE_CLASS_MAPPINGS"]
