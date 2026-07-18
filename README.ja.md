[English](README.md) · [繁體中文](README.zh-Hant.md) · [简体中文](README.zh-Hans.md) · **日本語**

# AIPaintWorks Tag Search（ComfyUI サイドバーツール）

自然言語（中／英／日）で説明 → 標準 Danbooru タグを、ComfyUI の CLIP Text Encode ノードへ
直接挿入。[AIPaintWorks](https://aipaintworks.com) タグ意味検索エンジンの ComfyUI フロントエンドです。

サイドバーパネルで意味検索（4 モード）、共起の関連おすすめ、投稿数での並べ替え、中/日/英の
名称と説明、NSFW ぼかし、タグをチェックして PROMPT を組み立て（重み付き）、指定した
CLIP Text Encode ノードの末尾へ挿入、またはクリップボードへコピー（タグ名の括弧は
`\(` `\)` に自動エスケープ）。

## クイックスタート

**必要環境：** ComfyUI（2024 年半ば以降）＋インターネット——検索はオンライン API `aipaintworks.com` を呼び出します（1 IP あたり 1 日 50 回）。

**インストール**（いずれか）：
- **ComfyUI-Manager** — `Tag Semantic Search`（発行者 AIPaintWorks）を検索 → Install → ComfyUI を再起動。黄色の「Pending Security Review」バッジは正常で、そのままインストールできます。
- **手動** — `git clone https://github.com/noirene0519/comfyui-aipaint-tags` を `ComfyUI/custom_nodes/` へ、その後再起動。

**使い方：** 左のツールバーの**本アイコン**をクリック → モードを選び説明を入力して Search → タグにチェック → CLIP Text Encode ノードを選んで Insert（または Copy all）。UI とタグの言語は ComfyUI の設定に従います。

## アーキテクチャ（ルート A：シンクライアント）

本ノードはエンジンやデータを**内蔵しません**——検索はすべてオンラインの AIPaintWorks API を呼び出します：

```
サイドバー JS  ──fetch──▶  ComfyUI バックエンド代理 /aipaint_tags/*  ──▶  オンライン AIPaintWorks API
（ブラウザ、同一オリジン）   （proxy.py、サーバ側 aiohttp）              （POST /search、/related）
```

フロントは同一オリジンの ComfyUI ルートのみを呼び、代理がサーバ側で転送——ブラウザの CORS を
回避し、エンドポイントも隠します。1 日のクォータは呼び出し元 IP 単位（公開サイトで 1 日 50 回の
異なる検索）。

## インストール

**必要条件：ComfyUI フロントエンド ≥ 1.2.4**（サイドバー Tabs API
`extensionManager.registerSidebarTab`。2024 年半ば以降の ComfyUI なら概ね満たします）。

- **Comfy Registry（推奨）**：ComfyUI-Manager で `Tag Semantic Search`（発行者 AIPaintWorks／
  `@noirene0519`）を検索してインストール（デフォルトのセキュリティ設定で可）。
- **Git URL**：Manager の「Install via Git URL」に本 repo の URL を入力。Manager の既定は
  `allow_git_url_install = false` かつループバックのみ有効——`config.ini` で
  `allow_git_url_install = true` に設定してください。
- **手動**：`ComfyUI/custom_nodes/` へ clone し、ComfyUI を再起動。

インストール後、左のツールバーに本アイコンのタブが出ます（ホバーでツール名を表示）。
**UI とタグ/説明の言語は ComfyUI 自身の言語設定に追従します**（Settings → Comfy.Locale；
繁体中国語/簡体中国語/日本語/英語、その他の言語は英語にフォールバック）。パネル自体に言語切替はありません。

## 設定

オンライン API のエンドポイントは環境変数で上書きできます（セルフホストやドメイン切替時）：

```bash
export AIPAINT_API_BASE="https://aipaintworks.com"   # 既定は移行期エンドポイント、proxy.py 参照
```

## 使い方

1. サイドバーの本アイコンのタブを開く。
2. モードを選び、（任意で）カテゴリ／NSFW、説明を入力して「検索」（または Ctrl/⌘+Enter）。
3. full_scene/concept 検索後に分割チップの行が出ます：クリックでその分割語の結果のみ表示、
   再クリックで解除。
4. 「結果／関連おすすめ」タブ切替：結果はチェックボックスで PROMPT に追加、投稿数で並べ替え、
   タグ名クリックで Danbooru を開く、⧉ で 1 タグをコピー、ホバーで説明；関連おすすめは
   選択中タグの共起提案です。
5. PROMPT 欄ではチップの ± で重み調整、× で削除；「リセット」は 2 段階確認で全消去。
6. 下のプルダウンで対象 CLIP Text Encode ノードを選び（開くたび再スキャン）、「挿入」でその
   テキスト末尾へ追記、または「全てコピー」で PROMPT 全体をクリップボードへ。

## ライセンスと出典

本ノードの**ソースコード**はプロプライエタリ——© 2026 AIPaintWorks。AIPaintWorks サービスと併せて
インストール・利用できますが、書面の許可なく再配布・改変はできません。**タグデータに対して
「all rights reserved」は主張しません**——データは [Danbooru](https://danbooru.donmai.us) および
[Bangumi](https://bgm.tv)（[CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)、ライセンスに従い
出典を明示）由来で、多言語名称と一部説明は LLM 生成のため参考用です。非公式ツールであり、
Danbooru／Bangumi とは無関係です。全文は [LICENSE](LICENSE) 参照。

---

> **メンテナ向け**：本ノードは AIPaintWorks ウェブ版の検索 UI の並行コピー（エンジンとデータはオンライン
> API のサーバー側、本 repo はシンクライアント）。UI 文言・括弧エスケープ・モード・API 契約はメンテナが
> アップストリームのウェブ版と同期します。
