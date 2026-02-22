---
name: web
description: Deploy and serve web apps via vite on port 49165.
---

Write files to /web/<app_name>/. Any dir with index.html is live:
  /web/myapp/index.html  →  https://krons.fiu.wtf/myapp/

## After every file edit under /web/

1. Fetch the affected URL (WebFetch or curl)
2. If error or timeout: kill $(cat /srv/app/tmp/vite.pid)
3. Wait 2s, verify again before reporting done

## /web/index.html

Root landing page listing all deployed apps.
- Update when adding or removing any app
- Only list apps the user explicitly asked for
- Never add placeholders or examples
