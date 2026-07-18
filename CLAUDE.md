# CLAUDE.md — AI 開工前必讀（本檔只做指針）

ComfyUI 側欄自訂節點：自然語言→Danbooru 標籤，插入 CLIP Text Encode。**路線 A 薄客戶端**——不內嵌引擎/資料，呼叫線上 AIPaintWorks API。

| 想知道 | 去讀 |
|---|---|
| 用法／安裝／架構 | [README.md](README.md) |
| 後端代理（轉呼線上 API、版本查詢） | [proxy.py](proxy.py) |
| 側欄面板全部 UI 與邏輯 | [js/aipaint_tags.js](js/aipaint_tags.js) |
| Registry 發布元資料／版號 | [pyproject.toml](pyproject.toml) |

## 紅線（違反必炸）

1. **這是網頁版前端的平行複製、非共用碼**——UI 四語字串、括號跳脫、模式清單、功能行為、API 合約讀取都各寫一份。**改功能/字串 → 需與上游網頁版同步**（上游維護於私有母專案；詳細同步點清單見維護者私有筆記，不在本公開 repo）；改完 bump `pyproject` version。
2. **API 端點**：`proxy.py` `DEFAULT_API_BASE`＝`https://aipaintworks.com`（域名 2026-07-17 上線 HTTPS；env `AIPAINT_API_BASE` 覆寫）。**換機（VPS IP 變）不必改此預設**（域名不動）；除非域名本身變更才要改預設並發新版。
3. **不臆測 ComfyUI API**：Sidebar Tabs／server 路由／Registry 等外部行為先查官方文件或實測（前端 ≥1.2.4；本版 loader 需空 `NODE_CLASS_MAPPINGS` 消 IMPORT FAILED 假警告）。
4. **改 `proxy.py`（後端路由）使用者端需重啟 ComfyUI 才生效**；純 `js/` 改動只需瀏覽器刷新。本機測試裝法＝junction 到 `ComfyUI/custom_nodes/`。
5. **發版**：bump `pyproject` version → push main → GitHub Action 自動發 Registry（secret `REGISTRY_ACCESS_TOKEN`）。純伺服器端改動（資料/搜尋邏輯/釋義）兩邊自動生效、無需發版。**發版時機（委託方 2026-07-18 定案）**：只在**大更新／修復／新增／調整**（實質功能變動）才 bump 版號發布；**其餘（純文件/metadata/授權/端點微調）不發，或先問委託方**——教訓：0.1.1–0.1.4 皆非功能改動卻各發一版，Registry「Updates」列表被灌成 5 版、觀感雜亂，委託方 2026-07-18 手動刪版收拾（見下）。**Registry 版本無法用 PAT 刪**：`pat-…` 只授權發布（放 POST body `personal_access_token`）；刪/棄用版本走 DELETE/PUT（BearerAuth＝網站 Firebase JWT），只能登入 registry.comfy.org 手動 unpublish，或抓網站現場 JWT 呼叫 API。→ **少發版＝少留爛帳，發版前想清楚**。

## 身份

git user＝noirene0519；分支 main。
