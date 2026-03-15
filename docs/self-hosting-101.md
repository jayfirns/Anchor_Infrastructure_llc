# Self-Hosting 101

## What Is Self-Hosting?

Self-hosting means running services on hardware you own instead of renting them from a cloud provider.

That's it. That's the whole concept.

When you use Gmail, Google runs the email server. When you use LastPass, LastPass stores your passwords. When you use Google DNS, your ISP (and Google) can see every website you visit.

When you self-host, **you** run the server. Your passwords live on a Raspberry Pi in your closet. Your DNS queries never leave your network. Your files sit on a hard drive you can physically touch.

## Why Would Anyone Do This?

### Privacy

Every cloud service you use is a company that stores your data on their terms. They can read it, mine it, sell insights about it, change the terms of service, get breached, or shut down entirely. Self-hosting removes the middleman.

### Cost

A Raspberry Pi costs $60 once. A repurposed laptop costs $0. The software is free. Compare that to $3/month for a password manager + $10/month for monitoring + $5/month for cloud storage + whatever Google is charging for the privilege of reading your email.

### Control

No one can cancel your account. No one can change the pricing. No one can discontinue the product. If it runs on your hardware, it runs until you decide otherwise.

### Learning

This is how the internet actually works. Every website, every app, every service — it's software running on a computer somewhere. Self-hosting pulls back the curtain and shows you the machinery. That knowledge has value whether you end up running everything yourself or not.

## What Do I Need?

### Hardware (Pick One)

| Option | Cost | Notes |
|--------|------|-------|
| **Raspberry Pi 4/5** | $60-100 | Small, quiet, low power. The classic choice. |
| **Old laptop** | Free | Already has a screen, keyboard, and battery (free UPS). Stick it in a closet. |
| **Mini PC** | $150-300 | More power than a Pi, smaller than a laptop. Good middle ground. |
| **Any computer** | Varies | If it turns on, has 4GB+ RAM, and connects to ethernet, it works. |

### Software

- A Linux-based operating system (Ubuntu Server, Debian, Raspberry Pi OS)
- Docker and Docker Compose (packages software so it runs the same everywhere)
- The services you want to run (all free, all open source)

### Knowledge

You're building it right now by reading this.

## Is This Actually Practical?

Yes. Millions of people self-host. The software is mature, well-documented, and actively maintained by large open-source communities. Services like Pi-hole, Vaultwarden, and Uptime Kuma have been running in production environments for years.

The real question isn't whether self-hosting works — it's whether you want to be responsible for keeping it running. Software needs updates. Hardware can fail. Backups need to be configured and tested. There's a reason "managed services" is an industry.

But here's the thing: you don't have to go all-in. Start with one service. Block some ads with Pi-hole. See how it feels. If you love it, add more. If you decide you want someone else to handle the maintenance, [that's an option too](../proposal-generator/).

## Next Steps

- **[Docker Basics](docker-basics.md)** — Learn just enough Docker to run real services
- **[Johnny's Favorite Containers](johnnys-favorites.md)** — See what we actually run and why
- **[Try the Seed Stack](../seed-stack/)** — Three services, one command, zero cloud dependencies
