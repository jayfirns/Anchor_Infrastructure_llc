# Scent of Freedom

**You control your data. For free.**

Every photo you store, every password you save, every search you make — it lives on a computer somewhere. Right now, that computer probably belongs to Google, Apple, Microsoft, or Amazon. It doesn't have to.

Self-hosting means running your own services on your own hardware. Your passwords stay in your house. Your DNS queries don't get sold. Your monitoring dashboard doesn't cost $30/month. And nobody can change the terms of service on you overnight.

The software is free. The knowledge is free. This repo is here to show you the door.

---

## What's Here

### Learn

- **[Self-Hosting 101](docs/self-hosting-101.md)** — What self-hosting actually means, who it's for, and why it matters
- **[Docker Basics](docs/docker-basics.md)** — Just enough Docker to run real services. No CS degree required.
- **[Johnny's Favorite Containers](docs/johnnys-favorites.md)** — The containers I actually run and why. Opinionated, practical, no fluff.

### Try It

The **[Seed Stack](seed-stack/)** is a ready-to-run Docker Compose setup with three services that replace cloud subscriptions you're probably paying for right now:

| Service | What It Does | What It Replaces |
|---------|-------------|-----------------|
| **Pi-hole** | Blocks ads and trackers at the DNS level for your whole network | Google DNS, your ISP's snooping |
| **Vaultwarden** | Self-hosted password manager, compatible with all Bitwarden apps | LastPass, 1Password, Dashlane |
| **Uptime Kuma** | Monitors your services and tells you when something's down | Pingdom, UptimeRobot, StatusCake |

```bash
cd seed-stack
cp .env.example .env    # Edit with your values
./setup.sh              # Checks prereqs, generates secrets, starts everything
./health-check.sh       # See what's running — and what's not configured yet
```

The health check will show you something like this:

```
Anchor Seed Stack — Health Check
══════════════════════════════════
[PASS] Pi-hole .............. responding
[PASS] Vaultwarden .......... responding
[PASS] Uptime Kuma .......... responding
[WARN] Backups .............. not configured
[WARN] Security hardening ... not applied
[WARN] Automatic updates .... not configured
══════════════════════════════════
3 passed, 3 warnings
```

Those warnings aren't bugs — they're the gap between "running" and "production-grade." Getting containers running is the fun part. Backups, security hardening, monitoring, updates, documentation, and disaster recovery? That's the work.

### Go Deeper

If you look at those warnings and think:

- **"I'll figure it out myself"** — respect. The [docs](docs/) will help, and every one of those warnings links to a guide.
- **"I'd rather pay someone who already knows"** — that's what [Anchor Infrastructure](https://anchorinfrastructure.com) does.

Run the **[Proposal Generator](proposal-generator/)** on your own machine. It's a local survey that assesses your situation and recommends a service tier — no data leaves your computer, no email required.

```bash
cd proposal-generator
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

---

## The Fine Print

- All software referenced here is **open source** and maintained by their respective communities. We just packaged it for convenience.
- The Seed Stack is provided **as-is** for educational and evaluation purposes. No warranty, no telemetry, no phone-home.
- **You** are responsible for your own hardware, network, and data. We're showing you the tools, not running them for you.
- Nothing in this repo collects data, sends analytics, or reports back to anyone. Clone it, fork it, disconnect from the internet and run it. It all still works.

## License

Educational content in this repo is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The Seed Stack scripts are MIT licensed. All referenced software retains its original license.
