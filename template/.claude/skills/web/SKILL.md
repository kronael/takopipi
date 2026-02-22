---
name: web
description: Deploy and serve web apps via vite.
---

Write files to /web/<app_name>/. Any dir with index.html is live:
  /web/myapp/index.html  ->  served at /myapp/

## Public URL

Read `WEB_HOST` from env to construct public URLs:
- NEVER use localhost URLs in messages to users
- ALWAYS use `https://$WEB_HOST/<app>/` for public links
- If WEB_HOST is unset, tell the user the app is deployed but
  don't fabricate a URL

## Stack

Vite MPA mode serves /web/ as static files. No build step needed.
- Vanilla HTML + CSS + JS/TS (vite handles TS natively)
- Shared assets in /web/assets/ (hub.css, hub.js)
- Each app is a subdirectory with its own index.html

## Template

Template files are in this skill at `template/`. On first deploy:
1. Copy template/*.json and template/vite.config.ts to /web/
2. Copy template/assets/ to /web/assets/
3. Copy template/index.html to /web/index.html (landing page)

hub.css provides dark/light theme, cards, grids, responsive layout.
hub.js provides theme toggle button.

## Styling

Use the shared hub.css variables and classes for consistency:
- `.hub-container` for page wrapper
- `.card`, `.card-title`, `.card-meta` for content cards
- `.grid` for auto-responsive grid layout
- CSS variables: `--accent`, `--bg`, `--fg`, `--card`, `--border`

For richer styling, add Tailwind CDN to individual apps:
```html
<script src="https://cdn.tailwindcss.com"></script>
```
Tailwind works alongside hub.css. Use it for layout utilities
(flex, grid, spacing, typography) while hub.css handles theming.

For interactive apps, add Alpine.js CDN:
```html
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3/dist/cdn.min.js"></script>
```
Alpine.js adds reactivity without a build step. Single-file apps.

## After every file edit under /web/

1. Fetch the affected URL (WebFetch or curl)
2. If error or timeout: kill $(cat /srv/app/tmp/vite.pid)
3. Wait 2s, verify again before reporting done

## /web/index.html

Root landing page listing all deployed apps.
- Update when adding or removing any app
- Only list apps the user explicitly asked for
- Never add placeholders or examples
