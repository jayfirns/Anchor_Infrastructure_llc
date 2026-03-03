# Anchor Infrastructure LLC

Customer-facing tools and services for Anchor Infrastructure.

## Modules

### [Proposal Generator](proposal-generator/)

Interactive discovery questionnaire and proposal generator. Prospects complete a survey, receive a scored tier recommendation, and can generate a formatted PDF proposal.

```bash
cd proposal-generator
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Open http://localhost:5000.

See [`proposal-generator/`](proposal-generator/) for full documentation.

## Future Modules

- Marketing site
- Client portal
