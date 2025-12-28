# phish-sim-lab 🎣  
### Educational Phishing Simulation Toolkit

`phish-sim-lab` is a **lightweight educational phishing simulation platform** built with **Flask + SQLite**.  
It is designed to demonstrate how **security awareness campaigns** work, using **unique tracking links**, **click logging**, and **campaign reports**, without collecting credentials or sensitive data.

> ⚠️ **Ethical use only**  
> This project is intended for **authorized training and learning environments**.  
> Do **NOT** use it for malicious activity.

---

## 📌 Why this project exists

This project was created to:
- demonstrate **phishing awareness workflows**
- practice **secure backend development**
- showcase **Python + Flask + SQLite** skills
- build a **realistic cybersecurity portfolio project**

It simulates **user interaction**, not exploitation.

---

## ✨ Features

- Local admin authentication
- Campaign creation:
  - name
  - description
  - email subject
  - HTML email template
- Upload targets via CSV
- Unique tracking link per target (`/t/<token>`)
- Click logging:
  - timestamp (UTC)
  - IP address (best effort)
  - user-agent (truncated)
- Dashboard with:
  - total targets
  - total clicks
  - click rate
- CSV export per campaign
- Educational landing page (no credential capture)

---

## 🧱 Tech Stack

- **Python 3.11+**
- **Flask**
- **SQLite**
- HTML / CSS (Jinja templates)

---

## 📂 Project Structure

```text
phish-sim-lab/
├── app.py
├── templates/
│   ├── login.html
│   ├── dashboard.html
│   └── email_template.html
├── static/
│   └── style.css
├── reports/              # CSV exports (gitignored)
├── requirements.txt
├── database.db           # local only (gitignored)
└── README.md

🚀 Getting Started

1️⃣ Clone the repository
git clone https://github.com/<YOUR_GITHUB_USER>/phish-sim-lab.git
cd phish-sim-lab

2️⃣ Create virtual environment & install dependencies
python -m venv .venv


Activate:

Windows:

.venv\Scripts\activate


Linux / macOS:

source .venv/bin/activate


Install dependencies:

pip install -r requirements.txt

3️⃣ Run the application
python app.py


Open in your browser:

http://127.0.0.1:5000

🔐 Admin Credentials
Default credentials
Username: admin
Password: admin123


⚠️ These are development defaults only.

🔒 Recommended: use environment variables

You can override credentials using environment variables.

Windows (PowerShell)
$env:PHISHSIM_ADMIN_USER="matheus"
$env:PHISHSIM_ADMIN_PASS="strong_password_here"
$env:PHISHSIM_SECRET_KEY="super_secret_key_here"
python app.py

Linux / macOS
export PHISHSIM_ADMIN_USER="matheus"
export PHISHSIM_ADMIN_PASS="strong_password_here"
export PHISHSIM_SECRET_KEY="super_secret_key_here"
python app.py

📄 Targets CSV Format

Required column:

email

Optional column:

name

Example:

name,email
Alice,alice@example.com
Bob,bob@example.com
Charlie,charlie@example.com

🧪 How to Use (Step-by-Step)
1️⃣ Login

Access the dashboard using admin credentials.

2️⃣ Create a campaign

Fill in:

Campaign name

Description

Email subject

HTML email body

Example HTML:

<h3>Hello,</h3>
<p>Please review the information below.</p>
<p><a href="#">Access now</a></p>

3️⃣ Upload targets

Upload the targets.csv

System generates unique tracking links per target

4️⃣ Simulate clicks

Copy any tracking URL

Open it in an incognito window

Landing page confirms simulation

5️⃣ Review metrics

Dashboard shows:

total targets

total clicks

click rate

6️⃣ Export report

Click export to download:

campaign_report.csv

📊 Metrics Explained

Total Clicks
Number of recorded click events (can exceed target count)

Click Rate
Percentage of targets who clicked at least once

This separation reflects real security awareness metrics.

🛡️ Security & Ethics

No credential capture

No real email sending

Tokens are random and non-guessable

Intended only for authorized awareness simulations

🧠 What this project demonstrates

Secure Flask backend design

SQLite schema management and migrations

CSV parsing and validation

Token-based tracking

Basic metrics calculation

Defensive coding & error handling

🗺️ Roadmap

Unique click rate vs total clicks separation in UI

SMTP email sending (safe / opt-in)

Campaign-specific landing pages

Docker support

RBAC (roles)

📸 Screenshots


<img width="1064" height="1094" alt="image" src="https://github.com/user-attachments/assets/b36e269d-6b40-48ae-a8b8-2b540b190de1" />
<img width="842" height="310" alt="image" src="https://github.com/user-attachments/assets/be8ae32c-241a-445f-a32d-e0a768d2af81" />


📜 License

This project is released for educational purposes.
Use responsibly.
