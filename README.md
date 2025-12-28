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
