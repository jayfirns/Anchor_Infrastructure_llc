"""Anchor Infrastructure — Proposal Generator

Interactive discovery questionnaire and proposal generator.
Run locally: python app.py → http://localhost:5000
"""

import os
import json
import uuid
import sqlite3
from datetime import datetime

from flask import Flask, jsonify, request, render_template, send_file, abort
from dotenv import load_dotenv

from scoring import score_survey
from proposal import generate_proposal

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key-change-in-production")
DB_PATH = os.getenv("DB_PATH", "sessions.db")


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            answers TEXT,
            scores TEXT,
            recommended_tier TEXT,
            client_name TEXT,
            contact_email TEXT,
            proposal_path TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

def load_json(filename):
    path = os.path.join(os.path.dirname(__file__), "data", filename)
    with open(path) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Routes — Pages
# ---------------------------------------------------------------------------

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/survey")
def survey():
    return render_template("survey.html")


@app.route("/results/<session_id>")
def results_page(session_id):
    return render_template("results.html", session_id=session_id)


# ---------------------------------------------------------------------------
# Routes — API
# ---------------------------------------------------------------------------

@app.route("/api/questions")
def api_questions():
    questions = load_json("questions.json")
    return jsonify(questions)


@app.route("/api/tiers")
def api_tiers():
    tiers = load_json("tiers.json")
    return jsonify(tiers)


@app.route("/api/submit", methods=["POST"])
def api_submit():
    data = request.get_json()
    if not data or "answers" not in data:
        return jsonify({"error": "Missing answers"}), 400

    answers = data["answers"]
    client_name = data.get("client_name", "Prospective Client")
    contact_email = data.get("contact_email", "")

    # Score the survey
    scoring_rubric = load_json("scoring.json")
    result = score_survey(answers, scoring_rubric)

    # Save session
    session_id = str(uuid.uuid4())[:8]
    conn = get_db()
    conn.execute(
        """INSERT INTO sessions
           (id, created_at, answers, scores, recommended_tier, client_name, contact_email)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            session_id,
            datetime.utcnow().isoformat(),
            json.dumps(answers),
            json.dumps(result),
            result["recommended_tier"],
            client_name,
            contact_email,
        ),
    )
    conn.commit()
    conn.close()

    # Send email notification if configured
    _notify_email(session_id, client_name, contact_email, result)

    return jsonify({"session_id": session_id, "results": result})


@app.route("/api/results/<session_id>")
def api_results(session_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Session not found"}), 404
    return jsonify({
        "session_id": row["id"],
        "created_at": row["created_at"],
        "client_name": row["client_name"],
        "contact_email": row["contact_email"],
        "scores": json.loads(row["scores"]),
        "recommended_tier": row["recommended_tier"],
        "proposal_path": row["proposal_path"],
    })


@app.route("/api/proposal/<session_id>/generate", methods=["POST"])
def api_generate_proposal(session_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Session not found"}), 404

    overrides = request.get_json() or {}

    pricing = load_json("pricing.json")
    tiers = load_json("tiers.json")
    scores = json.loads(row["scores"])

    pdf_path = generate_proposal(
        session_id=session_id,
        client_name=row["client_name"],
        scores=scores,
        pricing=pricing,
        tiers=tiers,
        overrides=overrides,
    )

    conn.execute(
        "UPDATE sessions SET proposal_path = ? WHERE id = ?",
        (pdf_path, session_id),
    )
    conn.commit()
    conn.close()

    return jsonify({"session_id": session_id, "proposal_path": pdf_path})


@app.route("/api/proposal/<session_id>/download")
def api_download_proposal(session_id):
    conn = get_db()
    row = conn.execute(
        "SELECT proposal_path, client_name FROM sessions WHERE id = ?",
        (session_id,),
    ).fetchone()
    conn.close()
    if not row or not row["proposal_path"]:
        abort(404)

    path = row["proposal_path"]
    if not os.path.exists(path):
        abort(404)

    filename = f"Anchor_Proposal_{row['client_name'].replace(' ', '_')}_{session_id}.pdf"
    return send_file(path, as_attachment=True, download_name=filename)


# ---------------------------------------------------------------------------
# Email notification
# ---------------------------------------------------------------------------

def _notify_email(session_id, client_name, contact_email, result):
    smtp_host = os.getenv("SMTP_HOST")
    if not smtp_host:
        return  # SMTP not configured — skip silently

    import smtplib
    from email.mime.text import MIMEText

    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_pass = os.getenv("SMTP_PASS", "")
    from_addr = os.getenv("SMTP_FROM", smtp_user)
    to_addr = os.getenv("NOTIFY_EMAIL", "")

    if not to_addr:
        return

    tier = result["recommended_tier"]
    body = (
        f"New discovery survey completed.\n\n"
        f"Organization: {client_name}\n"
        f"Contact: {contact_email or 'Not provided'}\n"
        f"Recommended Tier: {tier}\n"
        f"Session ID: {session_id}\n\n"
        f"Score Breakdown:\n"
    )
    for dim, score in result.get("dimensions", {}).items():
        body += f"  {dim}: {score}\n"

    msg = MIMEText(body)
    msg["Subject"] = f"Anchor — New Discovery: {client_name} ({tier})"
    msg["From"] = from_addr
    msg["To"] = to_addr

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            if smtp_user:
                server.login(smtp_user, smtp_pass)
            server.sendmail(from_addr, [to_addr], msg.as_string())
    except Exception as e:
        print(f"[email] Failed to send notification: {e}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    print(f"Anchor Proposal Generator — http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)
