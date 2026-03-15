# Johnny's Favorite Containers

These are containers I actually run. Not a theoretical list — these are services I use daily and would set up again from scratch without hesitating. Each one replaces something you're probably paying for or tolerating.

---

## The Essentials (Start Here)

### Pi-hole — DNS Ad Blocking

**What it does:** Blocks ads and trackers at the DNS level for every device on your network. Your phone, your laptop, your smart TV, your kid's tablet — all protected without installing anything on each device.

**What it replaces:** Browser ad blockers (which only work per-browser), your ISP's DNS (which logs your queries), Google DNS (same problem, different company).

**Why I love it:** You configure it once on your router as the DNS server and forget about it. Then one day you use someone else's wifi and remember what the internet looks like with ads. You never go back.

```yaml
pihole/pihole:latest
# Port 53 (DNS), Port 80 (admin UI)
# http://YOUR_IP/admin
```

### Vaultwarden — Password Manager

**What it does:** Self-hosted Bitwarden-compatible password manager. Works with all official Bitwarden apps and browser extensions. Full sync, TOTP generation, file attachments, organizations.

**What it replaces:** LastPass ($3/mo), 1Password ($3/mo), Dashlane ($5/mo), or worse — using the same password everywhere.

**Why I love it:** It's feature-complete Bitwarden without the $45/year subscription. Your passwords live on your hardware. The mobile app, browser extension, and desktop client all work perfectly because they're the official Bitwarden clients — Vaultwarden just speaks the same API.

```yaml
vaultwarden/server:latest
# Port 8080 (web UI)
# http://YOUR_IP:8080
```

### Uptime Kuma — Service Monitoring

**What it does:** Beautiful monitoring dashboard. Set up checks for any service — HTTP, TCP, DNS, ping, Docker containers. Get notifications when something goes down via email, Slack, Discord, Telegram, or 90+ other integrations.

**What it replaces:** Pingdom ($15/mo), UptimeRobot (limited free tier), StatusCake, or just not knowing something is broken until someone tells you.

**Why I love it:** It takes 2 minutes to set up and immediately shows you the health of everything you run. There's something deeply satisfying about seeing a wall of green uptime bars.

```yaml
louislam/uptime-kuma:latest
# Port 3001
# http://YOUR_IP:3001
```

---

## Level Two (Once You're Hooked)

### Nginx Proxy Manager — Reverse Proxy

**What it does:** Puts all your services behind clean URLs with HTTPS. Instead of remembering `192.168.1.50:8080`, you access `vault.home.local` with a proper SSL certificate.

**What it replaces:** Typing IP addresses and port numbers like a caveman.

**Why it matters:** This is the difference between "I have some containers running" and "I have a proper setup." Plus, HTTPS means your passwords aren't flying across your network in plaintext.

```yaml
jc21/nginx-proxy-manager:latest
# Port 81 (admin), Port 80 (HTTP), Port 443 (HTTPS)
```

### Tailscale — Mesh VPN

**What it does:** Creates a private network between your devices. Access your home services securely from anywhere — coffee shop, office, vacation — without opening ports on your router.

**What it replaces:** Port forwarding (insecure), traditional VPNs (painful), not being able to access your stuff remotely.

**Why I love it:** Zero configuration on the network side. Install it on your server and your phone. Done. Your home services are now reachable from anywhere as if you were on your local network.

```
# Not a container — installed on the host
# curl -fsSL https://tailscale.com/install.sh | sh
```

### Grafana + Prometheus — Metrics & Dashboards

**What it does:** Collects metrics from all your services and displays them in dashboards. CPU usage, memory, disk space, network traffic, container stats, custom application metrics.

**What it replaces:** Guessing. Task Manager. Hoping things are fine.

**Why it matters:** When something is slow or broken, you want to look at a graph and see exactly when it started, not ssh into a machine and run `top` while the problem is already gone.

```yaml
grafana/grafana:latest        # Dashboards — Port 3000
prom/prometheus:latest        # Metrics collection — Port 9090
```

---

## Honorable Mentions

| Container | What It Does | Why |
|-----------|-------------|-----|
| `nextcloud` | Self-hosted Google Drive/Docs | Own your files, calendars, contacts |
| `immich` | Self-hosted Google Photos | Photo backup and organization, looks great |
| `jellyfin` | Media server | Your movies, your music, no subscription |
| `actual-budget` | Budgeting tool | Mint/YNAB replacement, runs locally |
| `gitea` | Self-hosted GitHub | Private repos, no limits, your machine |
| `homepage` | Dashboard | One page linking to all your services |
| `watchtower` | Auto-updater | Watches for new container images and updates them |

---

## Where to Find More

- **[awesome-selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted)** — Massive curated list of self-hosted software
- **[r/selfhosted](https://reddit.com/r/selfhosted)** — Community of self-hosters sharing setups and advice
- **[LinuxServer.io](https://linuxserver.io)** — Well-maintained container images with consistent conventions
- **[Docker Hub](https://hub.docker.com)** — The app store for container images

---

## Ready to Try?

The **[Seed Stack](../seed-stack/)** bundles the three essentials (Pi-hole, Vaultwarden, Uptime Kuma) into a single `docker compose up` command. Start there.

If you try it, love it, and then stare at the health check warnings about backups and security and think "I don't want to deal with that" — the **[Proposal Generator](../proposal-generator/)** will help you figure out what level of help makes sense.
