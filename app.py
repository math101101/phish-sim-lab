import os
import csv
import sqlite3
import secrets
from datetime import datetime, timezone
from functools import wraps

from flask import (
    Flask, request, redirect, url_for, render_template,
    session, flash, send_file, abort
)

# ----------------------------
# Paths / Config
# ----------------------------
APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "database.db")
REPORTS_DIR = os.path.join(APP_DIR, "reports")
REPORT_PATH = os.path.join(REPORTS_DIR, "campaign_report.csv")

ADMIN_USER = os.getenv("PHISHSIM_ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("PHISHSIM_ADMIN_PASS", "admin123")  # altere em uso real

app = Flask(__name__)
app.secret_key = os.getenv("PHISHSIM_SECRET_KEY", secrets.token_hex(16))

print("DB_PATH =", DB_PATH)  # ajuda a confirmar qual banco está sendo usado


# ----------------------------
# DB Helpers
# ----------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def utc_iso() -> str:
    # ISO 8601 UTC timezone-aware
    return datetime.now(timezone.utc).isoformat()


def init_db():
    os.makedirs(REPORTS_DIR, exist_ok=True)

    conn = get_db()
    cur = conn.cursor()

    # campaigns (com description)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            email_subject TEXT NOT NULL,
            email_html TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # ✅ Migração: garante que coluna 'description' exista em bancos antigos
    cols = [row[1] for row in cur.execute("PRAGMA table_info(campaigns)").fetchall()]
    if "description" not in cols:
        cur.execute("ALTER TABLE campaigns ADD COLUMN description TEXT")

    # targets
    cur.execute("""
        CREATE TABLE IF NOT EXISTS targets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER NOT NULL,
            name TEXT,
            email TEXT NOT NULL,
            token TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL,
            FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
        )
    """)

    # clicks
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clicks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_id INTEGER NOT NULL,
            clicked_at TEXT NOT NULL,
            ip TEXT,
            user_agent TEXT,
            FOREIGN KEY (target_id) REFERENCES targets(id)
        )
    """)

    conn.commit()
    conn.close()


# ----------------------------
# Auth
# ----------------------------
def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapper


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username", "")
        pw = request.form.get("password", "")
        if user == ADMIN_USER and pw == ADMIN_PASS:
            session["logged_in"] = True
            session["username"] = user
            return redirect(url_for("dashboard"))
        flash("Credenciais inválidas.", "error")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ----------------------------
# Views
# ----------------------------
@app.route("/", methods=["GET"])
@login_required
def dashboard():
    conn = get_db()
    cur = conn.cursor()

    campaigns = cur.execute("""
        SELECT c.*,
          (SELECT COUNT(*) FROM targets t WHERE t.campaign_id = c.id) AS targets_count,
          (SELECT COUNT(*) FROM clicks ck
             JOIN targets t2 ON t2.id = ck.target_id
             WHERE t2.campaign_id = c.id) AS clicks_count
        FROM campaigns c
        ORDER BY c.id DESC
    """).fetchall()

    selected_id = request.args.get("campaign_id")
    selected = None
    targets = []
    click_rate = None

    if selected_id:
        selected = cur.execute("SELECT * FROM campaigns WHERE id = ?", (selected_id,)).fetchone()
        if selected:
            targets = cur.execute("""
                SELECT t.*,
                  (SELECT COUNT(*) FROM clicks ck WHERE ck.target_id = t.id) AS clicks
                FROM targets t
                WHERE t.campaign_id = ?
                ORDER BY t.id DESC
            """, (selected_id,)).fetchall()

            total_targets = len(targets)
            total_clicks = sum(int(t["clicks"]) for t in targets)
            click_rate = (total_clicks / total_targets * 100) if total_targets else 0.0

    conn.close()

    base_url = request.host_url.rstrip("/")
    return render_template(
        "dashboard.html",
        campaigns=campaigns,
        selected=selected,
        targets=targets,
        click_rate=click_rate,
        base_url=base_url
    )


# ----------------------------
# Actions
# ----------------------------
@app.route("/campaign/create", methods=["POST"])
@login_required
def create_campaign():
    try:
        name = (request.form.get("name") or "").strip()
        description = (request.form.get("description") or "").strip()
        subject = (request.form.get("email_subject") or "").strip()
        html = (request.form.get("email_html") or "").strip()

        if not name or not subject or not html:
            flash("Preencha: Nome da campanha, Assunto e HTML do email.", "error")
            return redirect(url_for("dashboard"))

        conn = get_db()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO campaigns (name, description, email_subject, email_html, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (name, description, subject, html, utc_iso()))

        conn.commit()
        campaign_id = cur.lastrowid
        conn.close()

        flash("Campanha criada com sucesso!", "ok")
        return redirect(url_for("dashboard", campaign_id=campaign_id))

    except Exception as e:
        print("🔥 ERRO AO CRIAR CAMPANHA:", repr(e))
        flash("Erro interno ao criar campanha. Veja o terminal.", "error")
        return redirect(url_for("dashboard"))


@app.route("/campaign/<int:campaign_id>/upload", methods=["POST"])
@login_required
def upload_targets(campaign_id: int):
    file = request.files.get("targets_csv")
    if not file:
        flash("Envie um arquivo CSV.", "error")
        return redirect(url_for("dashboard", campaign_id=campaign_id))

    content = file.read().decode("utf-8", errors="replace").splitlines()
    reader = csv.DictReader(content)

    if not reader.fieldnames or "email" not in reader.fieldnames:
        flash("CSV inválido. Precisa ter ao menos a coluna: email (e opcional name).", "error")
        return redirect(url_for("dashboard", campaign_id=campaign_id))

    rows = []
    for row in reader:
        email = (row.get("email") or "").strip()
        name = (row.get("name") or "").strip()
        if not email:
            continue
        rows.append((name, email))

    if not rows:
        flash("Nenhum target válido encontrado no CSV.", "error")
        return redirect(url_for("dashboard", campaign_id=campaign_id))

    conn = get_db()
    cur = conn.cursor()

    camp = cur.execute("SELECT id FROM campaigns WHERE id = ?", (campaign_id,)).fetchone()
    if not camp:
        conn.close()
        abort(404)

    inserted = 0
    for name, email in rows:
        token = secrets.token_urlsafe(16)
        # tenta inserir, se colidir token (improvável), tenta de novo maior
        for _ in range(2):
            try:
                cur.execute("""
                    INSERT INTO targets (campaign_id, name, email, token, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (campaign_id, name, email, token, utc_iso()))
                inserted += 1
                break
            except sqlite3.IntegrityError:
                token = secrets.token_urlsafe(24)

    conn.commit()
    conn.close()

    flash(f"Targets importados: {inserted}", "ok")
    return redirect(url_for("dashboard", campaign_id=campaign_id))


@app.route("/campaign/<int:campaign_id>/export", methods=["GET"])
@login_required
def export_campaign(campaign_id: int):
    conn = get_db()
    cur = conn.cursor()

    camp = cur.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,)).fetchone()
    if not camp:
        conn.close()
        abort(404)

    data = cur.execute("""
        SELECT
          c.id AS campaign_id,
          c.name AS campaign_name,
          t.id AS target_id,
          t.name AS target_name,
          t.email AS target_email,
          t.token AS token,
          (SELECT COUNT(*) FROM clicks ck WHERE ck.target_id = t.id) AS clicks
        FROM targets t
        JOIN campaigns c ON c.id = t.campaign_id
        WHERE c.id = ?
        ORDER BY t.id ASC
    """, (campaign_id,)).fetchall()

    os.makedirs(REPORTS_DIR, exist_ok=True)
    with open(REPORT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "campaign_id", "campaign_name",
            "target_id", "target_name", "target_email",
            "token", "clicks", "tracking_url"
        ])
        base_url = request.host_url.rstrip("/")
        for r in data:
            tracking_url = f"{base_url}/t/{r['token']}"
            writer.writerow([
                r["campaign_id"], r["campaign_name"],
                r["target_id"], r["target_name"], r["target_email"],
                r["token"], r["clicks"], tracking_url
            ])

    conn.close()
    return send_file(REPORT_PATH, as_attachment=True, download_name="campaign_report.csv")


@app.route("/email/<int:campaign_id>", methods=["GET"])
@login_required
def preview_email(campaign_id: int):
    conn = get_db()
    cur = conn.cursor()
    camp = cur.execute("SELECT * FROM campaigns WHERE id = ?", (campaign_id,)).fetchone()
    conn.close()
    if not camp:
        abort(404)
    return render_template("email_template.html", campaign=camp)


@app.route("/t/<token>", methods=["GET"])
def track(token: str):
    conn = get_db()
    cur = conn.cursor()

    target = cur.execute("""
        SELECT t.*, c.name AS campaign_name
        FROM targets t
        JOIN campaigns c ON c.id = t.campaign_id
        WHERE t.token = ?
    """, (token,)).fetchone()

    if not target:
        conn.close()
        return "Invalid token.", 404

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent", "")

    cur.execute("""
        INSERT INTO clicks (target_id, clicked_at, ip, user_agent)
        VALUES (?, ?, ?, ?)
    """, (target["id"], utc_iso(), ip, (ua or "")[:500]))
    conn.commit()
    conn.close()

    # Landing page educativa (sem coleta de credenciais)
    now = utc_iso()
    return f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1"/>
        <title>Simulação Educacional</title>
        <style>
          body {{ font-family: Arial, sans-serif; padding: 24px; max-width: 820px; margin: 0 auto; }}
          .card {{ border: 1px solid #e5e5e5; border-radius: 12px; padding: 18px; }}
          .ok {{ color: #0a7; font-weight: bold; }}
          code {{ background: #f6f6f6; padding: 2px 6px; border-radius: 6px; }}
        </style>
      </head>
      <body>
        <h2 class="ok">✅ Simulação de Phishing (Awareness)</h2>
        <div class="card">
          <p>Você clicou em um link de <strong>simulação educacional</strong> da campanha: <strong>{target['campaign_name']}</strong>.</p>
          <p>Isso não coletou senha, dados pessoais ou credenciais. O objetivo é conscientização.</p>
          <ul>
            <li>Confira o remetente e o domínio</li>
            <li>Passe o mouse no link antes de clicar</li>
            <li>Desconfie de urgência (“agora ou nunca”)</li>
            <li>Reporte ao time de segurança quando tiver dúvida</li>
          </ul>
          <p><small>Registro (UTC): <code>{now}</code></small></p>
        </div>
      </body>
    </html>
    """


# ----------------------------
# Main
# ----------------------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
