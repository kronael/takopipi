# TODO: takopipi

**Concept**: batteries-included, self-provisioning agent hub.
One container spins up a Telegram bot that provisions itself --
discovers projects, wires agents to web deployments, and gives
the operator a mobile-first interface to their own infrastructure.

No SaaS. No dashboard. Your phone, your server, your agents.

---

## Backlog

### core
- [ ] self-ident: add notes on agent self-identification
- [ ] improve /about: richer agent description and capabilities
- [ ] multi-instance: one bot token per user, shared container
- [ ] project hot-reload: re-discover /web without full restart
- [ ] agent session persistence: survive container restart

### web deploy
- [ ] nginx reverse proxy per app (subdomain or subpath)
- [ ] SSL termination for deployed apps
- [ ] build step: detect package.json and run npm build

### plugins
- [ ] /status: show vite PID, uptime, active sessions
- [ ] /deploy <app>: manual trigger for build + serve
- [ ] /log <app>: tail last N lines of app logs

### ops
- [ ] Dockerfile: pin node version alongside python
- [ ] healthcheck endpoint for container orchestrator
- [ ] log rotation for vite and takopi output

---
