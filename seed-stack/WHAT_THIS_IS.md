# What This Is (And Isn't)

## What This Is

This is a convenience package of three open-source services, configured to work together out of the box. We didn't write any of this software — we packaged it because we use it and think you should too.

### The Services

| Service | Upstream Project | License |
|---------|-----------------|---------|
| Pi-hole | [github.com/pi-hole/pi-hole](https://github.com/pi-hole/pi-hole) | EUPL-1.2 |
| Vaultwarden | [github.com/dani-garcia/vaultwarden](https://github.com/dani-garcia/vaultwarden) | AGPL-3.0 |
| Uptime Kuma | [github.com/louislam/uptime-kuma](https://github.com/louislam/uptime-kuma) | MIT |

All credit goes to those projects and their communities.

## What This Isn't

- **Not a product.** There's no company behind this stack, no support contract, no SLA. It's free software packaged for convenience.
- **Not managed.** Nobody is monitoring this, updating it, or backing it up unless you set that up yourself.
- **Not hardened.** The default configuration prioritizes "get it running" over "lock it down." Security hardening is your responsibility.
- **Not production-grade.** Running three containers is a start. Backups, monitoring, security, updates, and documentation are what make it production-grade.

## What It Does NOT Do

- Does not send data off your machine
- Does not collect telemetry or analytics
- Does not phone home to any server
- Does not modify system configuration outside of Docker
- Does not open firewall ports
- Does not require an internet connection after initial image download

## Your Responsibilities

- **Hardware:** You provide it, you maintain it, you power it
- **Network:** You configure DNS settings on your router
- **Updates:** You run `docker compose pull && docker compose up -d` when you want updates
- **Backups:** You configure backup for the Docker volumes (the data)
- **Security:** You harden the host OS and manage access

## Want Help?

If this is exciting but the maintenance part sounds like work, that's the gap between "running" and "managed." Anchor Infrastructure does the managed part.

Run the [Proposal Generator](../proposal-generator/) to see what tier of service fits your situation. It runs locally — no data leaves your machine.
