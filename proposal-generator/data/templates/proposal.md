# Infrastructure Proposal

**Prepared for:** {{ client_name }}
**Date:** {{ date }}
**Prepared by:** Anchor Infrastructure

---

## Executive Summary

Based on our discovery assessment, we recommend **{{ recommended_tier }}** for {{ client_name }}.

{{ reasoning }}

---

## Recommended Service: {{ recommended_tier }}

{{ tier.summary }}

### What You Get

{% for item in tier.included %}
- {{ item }}
{% endfor %}

### What Is Not Included

{% for item in tier.not_included %}
- {{ item }}
{% endfor %}

---

## How It Works

### 1. Discovery

We learn your business, assess your existing infrastructure, identify risks, and define what success looks like. Deliverable: discovery report with findings and recommendations.

### 2. Design

We propose an architecture that meets your requirements within your constraints. Every design decision is documented with tradeoffs explained. Deliverable: architecture document and project scope.

### 3. Build

We deploy infrastructure, harden it to our security baseline, configure backups and monitoring, and verify everything works — including a restore test. Deliverable: system baseline document and verified backup evidence.

### 4. Operate

Ongoing management: patching, monitoring, incident response, periodic security reviews, and disaster recovery drills. Deliverable: monthly reports, change logs, and DR drill evidence.

**Estimated timeline:** {{ tier.timeline }}

---

## Pricing

### One-Time Fees

| Item | Amount |
|------|--------|
| Discovery fee | ${{ pricing.discovery_fee.default | int }} |
| Implementation fee | ${{ pricing.implementation_fee.default | int }} |
{% if pricing.hardware_estimate %}| Hardware (estimated) | ${{ pricing.hardware_estimate.min | int }}-${{ pricing.hardware_estimate.max | int }} |{% endif %}

{{ pricing.hardware_estimate.note if pricing.hardware_estimate.note }}

### Monthly Retainer

| Item | Amount |
|------|--------|
| Monthly retainer | ${{ pricing.monthly_retainer.default | int }}/month |
| Included hours | {{ pricing.included_hours.default }} hours/month |
| Overage rate | ${{ pricing.overage_rate.default | int }}/hour |

### Estimated First-Year Cost

| Component | Amount |
|-----------|--------|
| One-time fees | ${{ (pricing.discovery_fee.default + pricing.implementation_fee.default) | int }} |
| Annual retainer (12 months) | ${{ (pricing.monthly_retainer.default * 12) | int }} |
| **Estimated total** | **${{ (pricing.discovery_fee.default + pricing.implementation_fee.default + pricing.monthly_retainer.default * 12) | int }}** |

*Hardware costs, if applicable, are in addition to the above. All hardware is purchased at cost with receipts provided. You own all hardware.*

*Pricing is based on the scope described in this proposal. Final pricing is confirmed after the discovery phase when the full environment is assessed. All ranges reflect typical engagements — your specific engagement may fall outside these ranges depending on complexity.*

---

## Service Level Summary

| Metric | Target |
|--------|--------|
{% for key, value in tier.sla.items() %}| {{ key | replace('_', ' ') | title }} | {{ value }} |
{% endfor %}

*Full SLA terms are documented in the service agreement, including exclusions, severity definitions, and client responsibilities.*

---

## Next Steps

1. **Sign the service agreement** — defines scope, SLA, and terms
2. **Schedule the discovery deep-dive** — we assess your full environment on-site or remotely
3. **Access provisioning** — secure credential exchange and system access verification
4. **Build begins** — security baseline, backups, monitoring, and documentation
5. **Go-live** — verified, documented, and operational

---

## About Anchor Infrastructure

Anchor Infrastructure designs, builds, and operates private and hybrid infrastructure for small organizations. We help clients take ownership of their technology — on hardware they control, with documented security baselines, tested disaster recovery, and full operational transparency.

Every system we manage comes with a baseline document, a recovery plan, and proof that both are current.

- **Own your infrastructure.** Your servers, your data, your documentation.
- **Recover with confidence.** Every backup plan is tested with documented evidence.
- **See what is happening.** Monitoring dashboards, change logs, and status reports.
- **Exit-ready by design.** If the engagement ends, you retain everything needed to continue independently.

---

*This proposal is valid for 30 days from the date above. Pricing and scope are subject to confirmation after the discovery phase.*

*Proposal ID: {{ session_id }}*
