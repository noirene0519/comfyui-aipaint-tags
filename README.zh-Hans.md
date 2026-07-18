[English](README.md) · [繁體中文](README.zh-Hant.md) · **简体中文** · [日本語](README.ja.md)

# AIPaintWorks 标签搜索（ComfyUI 侧栏工具）

用自然语言（中／英／日）描述 → 标准 Danbooru 标签，直接插入 ComfyUI 的 CLIP Text Encode
节点。[AIPaintWorks](https://aipaintworks.com) 标签语义搜索引擎的 ComfyUI 前端。

侧栏面板可语义搜索（四模式）、看共现关联推荐、按投稿数排序、看中/日/英名称与释义、
NSFW 遮蔽、勾选标签组成 PROMPT（可调权重），再一键附加到指定 CLIP Text Encode 节点的
文字尾端，或复制到剪贴板（tag 内括号自动转义为 `\(` `\)`）。

## 快速开始

**需求：** ComfyUI（2024 年中以后版本）＋可联网——搜索会调用线上 API `aipaintworks.com`（每 IP 每日 50 次）。

**安装**（择一）：
- **ComfyUI-Manager** — 搜索 `Tag Semantic Search`（发布者 AIPaintWorks）→ Install → 重启 ComfyUI。若显示黄色「Pending Security Review」标记属正常，仍可正常安装。
- **手动** — 把 `git clone https://github.com/noirene0519/comfyui-aipaint-tags` clone 进 `ComfyUI/custom_nodes/`，再重启。

**开始用：** 左侧工具栏点**书本图标** → 选模式、输入描述、按 Search → 勾选标签 → 选一个 CLIP Text Encode 节点按 Insert（或 Copy all）。界面与标签语言跟随 ComfyUI 本身设置。

## 架构（路线 A：瘦客户端）

本节点**不内嵌**引擎与数据——所有检索调用线上 AIPaintWorks API：

```
侧栏面板 JS  ──fetch──▶  ComfyUI 后端代理 /aipaint_tags/*  ──▶  线上 AIPaintWorks API
（浏览器，同源）          （proxy.py，服务器端 aiohttp）        （POST /search、/related）
```

前端只打 ComfyUI 同源路由，代理在服务器端转呼线上 API——避开浏览器 CORS、端点不外露。
每日配额按调用端 IP 计（线上站每日 50 次不同搜索）。

## 安装

**需求：ComfyUI 前端 ≥ 1.2.4**（侧栏 Tabs API `extensionManager.registerSidebarTab` 自此版起可用；
一般 2024 年中以后的 ComfyUI 皆满足）。

- **Comfy Registry（建议）**：ComfyUI-Manager 搜索 `Tag Semantic Search`（发布者 AIPaintWorks／`@noirene0519`）安装（默认安全设置即可）。
- **Git URL**：Manager「Install via Git URL」填本 repo 网址。注意 Manager 默认 `allow_git_url_install = false`
  且仅回环地址生效——须在 `config.ini` 设 `allow_git_url_install = true`。
- **手动**：clone 到 `ComfyUI/custom_nodes/`，重启 ComfyUI。

装好后左侧工具栏出现书本图标分页（滑入显示工具名）。**界面与标签/释义语言自动跟随 ComfyUI 的语言设置**
（Settings → Comfy.Locale；繁中/简中/日本語/English，其余语系退英文），面板本身无语言选项。

## 设置

线上 API 端点以环境变量覆盖（自建服务或域名切换时）：

```bash
export AIPAINT_API_BASE="https://aipaintworks.com"   # 默认为过渡态端点，见 proxy.py
```

## 用法

1. 开侧栏书本图标分页。
2. 选模式、（可选）分类／NSFW，输入描述，按「搜索」（或 Ctrl/⌘+Enter）。
3. full_scene/concept 搜索后上方出现切分 chip：点某词只显示该来源结果、再点取消。
4. 「结果／关联推荐」分页切换：结果 checkbox 勾选加入 PROMPT、可按投稿数排序、点标签名开 Danbooru、
   ⧉ 复制单一标签、滑入显释义；关联推荐是已选标签的共现建议。
5. PROMPT 区 chip 上 ± 调权重、× 移除；「重置」两段防呆清空。
6. 下方下拉选目标 CLIP Text Encode 节点（点开自动重扫），按「插入」附加到其文字尾端；
   或「复制全部」把整串 PROMPT 复制到剪贴板。

## 授权与署名

节点**源代码**为专有——© 2026 AIPaintWorks；可搭配 AIPaintWorks 服务安装使用，未经书面许可不得再散布
或改作。**不对标签数据主张 all rights reserved**——数据取自 [Danbooru](https://danbooru.donmai.us) 与
[Bangumi](https://bgm.tv)（采 [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/)、依授权标示来源）；
多语名称与部分释义由 LLM 生成、仅供参考。本工具为非官方，与 Danbooru／Bangumi 无隶属。全文见 [LICENSE](LICENSE)。

---

> **维护者**：本节点是 AIPaintWorks 网页版搜索 UI 的平行复制（引擎与数据在线上 API 后端、本 repo 为瘦客户端）；
> UI 字符串、括号转义、模式、API 合约由维护者与上游网页版同步。
