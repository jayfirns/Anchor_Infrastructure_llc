# Anchor Proposal Generator

Interactive discovery questionnaire and proposal generator for [Anchor Infrastructure](https://github.com/jayfirns/Anchor_Infrastructure). Prospects complete a survey, receive a scored tier recommendation, and can generate a formatted PDF proposal.

Runs locally — no cloud dependencies, no external API calls, no CDN.

## Quick Start

```bash
git clone https://github.com/jayfirns/anchor-proposal-generator.git
cd anchor-proposal-generator
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Open [http://localhost:5000](http://localhost:5000).

## How It Works

1. **Landing page** introduces Anchor Infrastructure's value pillars
2. **Discovery survey** walks prospects through 5 categories (16 questions)
3. **Scoring engine** evaluates answers across 5 dimensions and recommends a service tier
4. **Results page** shows the recommendation with reasoning and deliverables
5. **Proposal generator** produces a formatted PDF with pricing, SLA summary, and next steps

## Architecture

```
anchor-proposal-generator/
├── app.py                  # Flask application
├── scoring.py              # Scoring engine (deterministic, explainable)
├── proposal.py             # Markdown → PDF proposal generator
├── data/
│   ├── questions.json      # Question bank (5 categories, 16 questions)
│   ├── scoring.json        # Scoring rubric and tier thresholds
│   ├── tiers.json          # Tier definitions (Node / Hybrid / Enterprise)
│   ├── pricing.json        # Pricing bands, factors, and add-ons
│   └── templates/
│       ├── proposal.md     # Jinja2 proposal template
│       └── proposal.css    # PDF stylesheet
├── static/
│   ├── css/style.css       # UI stylesheet
│   └── js/
│       ├── survey.js       # Survey flow logic
│       └── results.js      # Results display and proposal generation
├── templates/              # Jinja2 HTML templates
│   ├── base.html
│   ├── landing.html
│   ├── survey.html
│   └── results.html
├── proposals/              # Generated proposals (gitignored)
├── requirements.txt
├── .env.example
└── .gitignore
```

## Survey Categories

| Category | Questions | Assesses |
|----------|-----------|----------|
| Organization Profile | 3 | Org type, size, data sensitivity |
| Current Infrastructure | 4 | Setup, services, provider, pain points |
| Security Posture | 4 | Incidents, backup confidence, compliance, privacy |
| Availability and Recovery | 3 | Downtime impact, data loss tolerance, redundancy |
| Budget and Priorities | 3 | Monthly budget, hardware, success metrics |

## Scoring Dimensions

| Dimension | Weight | Drives |
|-----------|--------|--------|
| Complexity | 1.0x | Service count, org size, environment type |
| Security | 1.5x | Data sensitivity, compliance, incidents, privacy |
| Availability | 1.5x | Downtime impact, RPO, geographic redundancy |
| Maturity | 0.5x | Current provider, known pain points |
| Budget | 0.5x | Monthly budget alignment |

## Tier Thresholds

| Score Range | Recommended Tier |
|-------------|------------------|
| 0-4 | Anchor Seed |
| 5-9 | Anchor Node |
| 10-17 | Anchor Hybrid |
| 18+ | Anchor Enterprise |

## Configuration

All configuration is in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Bind address | `127.0.0.1` |
| `PORT` | Listen port | `5000` |
| `SECRET_KEY` | Flask secret key | `dev-key-change-in-production` |
| `DB_PATH` | SQLite database path | `sessions.db` |
| `SMTP_HOST` | Email notification server | (disabled) |
| `NOTIFY_EMAIL` | Email address for survey notifications | (disabled) |

## Email Notifications

When `SMTP_HOST` is configured, the app sends an email notification when a prospect completes the survey. The email includes organization name, recommended tier, and score summary.

If SMTP is not configured, email is silently skipped.

## PDF Generation

Proposals are generated using `weasyprint` (Markdown → HTML → PDF). If `weasyprint` is not installed, the proposal is saved as HTML instead.

On some systems, `weasyprint` requires system-level dependencies:

```bash
# Debian/Ubuntu
sudo apt install -y libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0

# macOS
brew install pango
```

## Data Files

All business logic is in JSON files under `data/`. To adjust questions, scoring, pricing, or tier definitions, edit the JSON — no code changes needed.

| File | Purpose |
|------|---------|
| `questions.json` | Question bank with categories and options |
| `scoring.json` | Scoring rubric, tier thresholds, segment mapping, reasoning templates |
| `tiers.json` | Tier definitions, deliverables, SLA summaries |
| `pricing.json` | Pricing bands, adjustment factors, add-ons |

## Relationship to Anchor_Infrastructure

This tool is the customer-facing complement to the [Anchor Infrastructure operational playbook](https://github.com/jayfirns/Anchor_Infrastructure). The playbook documents how we operate internally. This tool faces outward — it qualifies prospects, recommends service tiers, and generates proposals using approved language from the playbook.

| Playbook Doc | Used By This Tool |
|--------------|-------------------|
| `SERVICE_TIERS.md` | Tier definitions in `tiers.json` |
| `PRICING_MODEL.md` | Pricing bands in `pricing.json` |
| `CLIENT_TYPES.md` | Discovery questions in `questions.json` |
| `MESSAGING_EXTERNAL.md` | Landing page copy, proposal language |
| `BRAND_POSITIONING.md` | Terminology, language guide |
| `SLA_TEMPLATE.md` | SLA summaries in tier data |
