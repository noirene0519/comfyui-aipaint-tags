[English](README.md) · **繁體中文** · [简体中文](README.zh-Hans.md) · [日本語](README.ja.md)

# AIPaintWorks 標籤搜尋（ComfyUI 側欄工具）

用自然語言（中／英／日）描述 → 標準 Danbooru 標籤，直接插入 ComfyUI 的 CLIP Text Encode
節點。[AIPaintWorks](https://aipaintworks.com) 標籤語義搜尋引擎的 ComfyUI 前端。

側欄面板可語義搜尋（四模式）、看共現關聯推薦、依貼文數排序、看中/日/英名稱與釋義、
NSFW 遮蔽、勾選標籤組成 PROMPT（可調權重），再一鍵附加到指定 CLIP Text Encode 節點的
文字尾端，或複製到剪貼簿（tag 內括號自動跳脫為 `\(` `\)`）。

## 快速開始

**需求：** ComfyUI（2024 年中以後版本）＋可連網——搜尋會呼叫線上 API `aipaintworks.com`（每 IP 每日 50 次）。

**安裝**（擇一）：
- **ComfyUI-Manager** — 搜尋 `Tag Semantic Search`（發布者 AIPaintWorks）→ Install → 重啟 ComfyUI。若顯示黃色「Pending Security Review」標記屬正常，仍可正常安裝。
- **手動** — 把 `git clone https://github.com/noirene0519/comfyui-aipaint-tags` clone 進 `ComfyUI/custom_nodes/`，再重啟。

**開始用：** 左側工具列點**書本圖示** → 選模式、輸入描述、按 Search → 勾選標籤 → 選一個 CLIP Text Encode 節點按 Insert（或 Copy all）。介面與標籤語言跟隨 ComfyUI 本身設定。

## 架構（路線 A：薄客戶端）

本節點**不內嵌**引擎與資料——所有檢索呼叫線上 AIPaintWorks API：

```
側欄面板 JS  ──fetch──▶  ComfyUI 後端代理 /aipaint_tags/*  ──▶  線上 AIPaintWorks API
（瀏覽器，同源）          （proxy.py，伺服器端 aiohttp）        （POST /search、/related）
```

前端只打 ComfyUI 同源路由，代理在伺服器端轉呼線上 API——避開瀏覽器 CORS、端點不外露。
日配額按呼叫端 IP 計（線上站每日 50 次不同搜尋）。

## 安裝

**需求：ComfyUI 前端 ≥ 1.2.4**（側欄 Tabs API `extensionManager.registerSidebarTab` 自此版起可用；
一般 2024 年中以後的 ComfyUI 皆滿足）。

- **Comfy Registry（建議）**：ComfyUI-Manager 搜尋 `Tag Semantic Search`（發布者 AIPaintWorks／`@noirene0519`）安裝（預設安全設定即可）。
- **Git URL**：Manager「Install via Git URL」填本 repo 網址。注意 Manager 預設 `allow_git_url_install = false`
  且僅回環位址生效——須在 `config.ini` 設 `allow_git_url_install = true`。
- **手動**：clone 到 `ComfyUI/custom_nodes/`，重啟 ComfyUI。

裝好後左側工具列出現書本圖示分頁（滑入顯示工具名）。**介面與標籤/釋義語言自動跟隨 ComfyUI 的語言設定**
（Settings → Comfy.Locale；繁中/简中/日本語/English，其餘語系退英文），面板本身無語言選項。

## 設定

線上 API 端點以環境變數覆寫（自架服務或域名切換時）：

```bash
export AIPAINT_API_BASE="https://aipaintworks.com"   # 預設為過渡態端點，見 proxy.py
```

## 用法

1. 開側欄書本圖示分頁。
2. 選模式、（可選）分類／NSFW，輸入描述，按「搜尋」（或 Ctrl/⌘+Enter）。
3. full_scene/concept 搜尋後上方出現切分 chip：點某詞只顯示該來源結果、再點取消。
4. 「結果／關聯推薦」分頁切換：結果 checkbox 勾選加入 PROMPT、可依貼文數排序、點標籤名開 Danbooru、
   ⧉ 複製單一標籤、滑入顯釋義；關聯推薦是已選標籤的共現建議。
5. PROMPT 區 chip 上 ± 調權重、× 移除；「重置」兩段防呆清空。
6. 下方下拉選目標 CLIP Text Encode 節點（點開自動重掃），按「插入」附加到其文字尾端；
   或「複製全部」把整串 PROMPT 複製到剪貼簿。

## 授權與署名

節點**原始碼**為專有——© 2026 AIPaintWorks；可搭配 AIPaintWorks 服務安裝使用，未經書面許可不得再散布
或改作。**不對標籤資料主張 all rights reserved**——資料取自 [Danbooru](https://danbooru.donmai.us) 與
[Bangumi](https://bgm.tv)（採 [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)、依授權標示來源）；
多語名稱與部分釋義由 LLM 生成、僅供參考。本工具為非官方，與 Danbooru／Bangumi 無隸屬。全文見 [LICENSE](LICENSE)。

---

> **維護者**：本節點是 AIPaintWorks 網頁版搜尋 UI 的平行複製（引擎與資料在線上 API 後端、本 repo 為薄客戶端）；
> UI 字串、括號跳脫、模式、API 合約由維護者與上游網頁版同步。
