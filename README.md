**English** · [繁體中文](README.zh-Hant.md) · [简体中文](README.zh-Hans.md) · [日本語](README.ja.md)

# AIPaintWorks Tag Search (ComfyUI sidebar tool)

Describe what you want in natural language (Chinese / English / Japanese) → standard Danbooru
tags, inserted straight into a ComfyUI CLIP Text Encode node. A ComfyUI front-end for the
[AIPaintWorks](https://aipaintworks.com) tag semantic search engine.

The sidebar panel does semantic search (4 modes), co-occurrence related suggestions, sort by post
count, Chinese/Japanese/English names & descriptions, NSFW blur, ticking tags to build a PROMPT
(with weights), then appends to a chosen CLIP Text Encode node or copies to the clipboard
(parentheses in tag names auto-escaped to `\(` `\)`).

## Quick start

**Needs:** ComfyUI (mid-2024 or newer) + internet — searches call the online API `aipaintworks.com` (50 searches per IP per day).

**Install** (pick one):
- **ComfyUI-Manager** — search `Tag Semantic Search` (publisher AIPaintWorks) → Install → restart ComfyUI. A yellow "Pending Security Review" badge is normal; the node stays installable.
- **Manual** — `git clone https://github.com/noirene0519/comfyui-aipaint-tags` into `ComfyUI/custom_nodes/`, then restart.

**Use it:** click the book icon in the left toolbar → pick a mode, type a description, press Search → tick tags → choose a CLIP Text Encode node and Insert (or Copy all). The UI and tag language follow ComfyUI's own setting.

## Architecture (Route A: thin client)

The node does **not** bundle the engine or data — every search call goes to the online
AIPaintWorks API:

```
Sidebar panel JS  ──fetch──▶  ComfyUI backend proxy /aipaint_tags/*  ──▶  online AIPaintWorks API
(browser, same-origin)        (proxy.py, server-side aiohttp)            (POST /search, /related)
```

The front-end only calls a same-origin ComfyUI route; the proxy forwards server-side — avoiding
browser CORS and keeping the endpoint hidden. Daily quota is per caller IP (50 distinct searches
per day on the hosted site).

## Installation

**Requires ComfyUI frontend ≥ 1.2.4** (the Sidebar Tabs API `extensionManager.registerSidebarTab`;
any ComfyUI from mid-2024 onward qualifies).

- **Comfy Registry (recommended)**: in ComfyUI-Manager search `Tag Semantic Search` (publisher
  AIPaintWorks / `@noirene0519`) and install — works under default security settings.
- **Git URL**: Manager "Install via Git URL" with this repo's URL. Note Manager defaults
  `allow_git_url_install = false` and only honors it on loopback — set `allow_git_url_install = true`
  in `config.ini`.
- **Manual**: clone into `ComfyUI/custom_nodes/` and restart ComfyUI.

After install a book icon appears in the left toolbar (hover shows the tool name). **The UI and the
tag/description language follow ComfyUI's own language setting** (Settings → Comfy.Locale; Traditional
Chinese / Simplified Chinese / Japanese / English, other locales fall back to English). The panel has
no language selector of its own.

## Configuration

Override the online API endpoint via an environment variable (self-hosting or domain switch):

```bash
export AIPAINT_API_BASE="https://aipaintworks.com"   # default is the transitional endpoint, see proxy.py
```

## Usage

1. Open the book-icon tab in the sidebar.
2. Pick a mode, optionally category / NSFW, type a description, press Search (or Ctrl/⌘+Enter).
3. After a full_scene / concept search a row of segment chips appears: click one to show only that
   segment's results, click again to clear.
4. Switch the Results / Related tabs: in Results, tick a checkbox to add to PROMPT, sort by post
   count, click a tag name to open Danbooru, ⧉ to copy a single tag, hover for its description;
   Related is co-occurrence suggestions for your selected tags.
5. In the PROMPT area use ± on a chip to adjust weight, × to remove; Reset (two-step confirm) clears all.
6. Pick a target CLIP Text Encode node from the dropdown (rescans on open) and Insert to append to its
   text, or Copy all to put the whole PROMPT on the clipboard.

## Development

The panel front-end is a parallel copy of the AIPaintWorks web app's search UI — the search engine
and data live server-side behind the online API, so this repo is a thin client. UI strings (4
languages), tag-paren escaping, search modes and API-contract handling are reimplemented here and
kept in sync with the upstream web app by the maintainer. Server-side changes (data, search logic,
descriptions) take effect with no front-end change.

## License & attribution

The node's **source code** is proprietary — © 2026 AIPaintWorks; you may install and use it with the
AIPaintWorks service, but not redistribute or modify it without written permission. **No "all rights
reserved" is claimed over the tag data**, which derives from [Danbooru](https://danbooru.donmai.us) and
from [Bangumi](https://bgm.tv) (licensed [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/),
credited as the license requires); localized names/descriptions are LLM-generated and for reference only.
Unofficial tool, not affiliated with Danbooru or Bangumi. Full text in [LICENSE](LICENSE).
