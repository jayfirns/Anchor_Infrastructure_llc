"""Proposal generator — markdown templates → PDF output.

Uses Jinja2 for markdown templating and weasyprint for PDF rendering.
Falls back to HTML-only if weasyprint is not installed.
"""

import os
import json
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "data", "templates")
PROPOSALS_DIR = os.path.join(os.path.dirname(__file__), "proposals")
CSS_PATH = os.path.join(os.path.dirname(__file__), "data", "templates", "proposal.css")


def generate_proposal(
    session_id: str,
    client_name: str,
    scores: dict,
    pricing: dict,
    tiers: dict,
    overrides: dict | None = None,
) -> str:
    """Generate a PDF proposal from survey results.

    Args:
        session_id: Unique session identifier.
        client_name: Organization name.
        scores: Scored survey results from scoring engine.
        pricing: Pricing data from data/pricing.json.
        tiers: Tier definitions from data/tiers.json.
        overrides: Optional pricing overrides from the user.

    Returns:
        Path to the generated PDF file.
    """
    overrides = overrides or {}
    recommended_tier = scores["recommended_tier"]

    # Resolve tier data
    tier_key = _tier_key(recommended_tier)
    tier_data = tiers.get(tier_key, tiers.get("anchor_node", {}))
    tier_pricing = pricing.get(tier_key, pricing.get("anchor_node", {}))

    # Apply overrides
    for key, value in overrides.items():
        if key in tier_pricing:
            tier_pricing[key] = value

    # Build template context
    context = {
        "client_name": client_name,
        "date": datetime.utcnow().strftime("%B %d, %Y"),
        "recommended_tier": recommended_tier,
        "tier": tier_data,
        "pricing": tier_pricing,
        "scores": scores,
        "dimensions": scores.get("dimensions", {}),
        "reasoning": scores.get("reasoning", ""),
        "session_id": session_id,
    }

    # Render markdown from template
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("proposal.md")
    markdown_content = template.render(**context)

    # Convert to HTML
    try:
        import markdown
        html_body = markdown.markdown(
            markdown_content, extensions=["tables", "fenced_code"]
        )
    except ImportError:
        # Basic fallback — wrap in pre
        html_body = f"<pre>{markdown_content}</pre>"

    # Wrap in full HTML with CSS
    css = ""
    if os.path.exists(CSS_PATH):
        with open(CSS_PATH) as f:
            css = f.read()

    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>{css}</style>
</head>
<body>
{html_body}
</body>
</html>"""

    # Generate PDF
    os.makedirs(PROPOSALS_DIR, exist_ok=True)
    safe_name = client_name.replace(" ", "_").replace("/", "_")
    pdf_path = os.path.join(
        PROPOSALS_DIR, f"{safe_name}_{session_id}.pdf"
    )

    try:
        from weasyprint import HTML
        HTML(string=full_html).write_pdf(pdf_path)
    except ImportError:
        # Fallback: save as HTML
        pdf_path = pdf_path.replace(".pdf", ".html")
        with open(pdf_path, "w") as f:
            f.write(full_html)
        print("[proposal] weasyprint not installed — saved as HTML")

    return pdf_path


def _tier_key(tier_name: str) -> str:
    """Convert display name to data key."""
    return tier_name.lower().replace(" ", "_").replace("anchor_", "anchor_")
