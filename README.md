# phish-sim-lab 🎣
## Educational Phishing Simulation Toolkit

`phish-sim-lab` is an **educational phishing simulation platform** built with **Python, Flask, and SQLite**.
It was designed to demonstrate how **security awareness campaigns** work by generating **unique tracking links**, logging **click events**, and producing **campaign reports**, without collecting credentials or sensitive information.

> ⚠️ **Ethical use only**  
> This project is intended exclusively for **authorized training and educational environments**.  
> Do **NOT** use this tool for malicious or unauthorized activities.

---

## 📌 Project Goals

- Demonstrate phishing awareness workflows
- Practice secure backend development with Flask
- Simulate user interaction safely (no exploitation)
- Build a realistic cybersecurity portfolio project

---

## ✨ Features

- Local admin authentication
- Campaign creation:
  - Name
  - Description
  - Email subject
  - HTML email template
- Target import via CSV
- Unique tracking link per target (`/t/<token>`)
- Click logging:
  - Timestamp (UTC)
  - IP address (best effort)
  - User-Agent (truncated)
- Dashboard metrics:
  - Total targets
  - Total clicks
  - Click rate
- Campaign report export (CSV)
- Educational landing page (no credential capture)

---

## 🧱 Tech Stack

- Python 3.11+
- Flask
- SQLite
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
```
## 🚀 Getting Started

Prerequisites:
- Python 3.11+
- Git
Installation

Clone the repository:

- git clone https://github.com/<YOUR_GITHUB_USERNAME>/phish-sim-lab.git
cd phish-sim-lab


Create and activate a virtual environment:
Windows:
- python -m venv .venv
- .venv\Scripts\activate

Linux / macOS:
- python -m venv .venv
- source .venv/bin/activate


Install dependencies:
- pip install -r requirements.txt
- Running the Application
- Start the application with:
- python app.py


The application will be available at:
- http://127.0.0.1:5000

## 🔐 Authentication & Credentials

Default Credentials (Development Only):
- Username: admin
- Password: admin123
Environment Variables (Recommended)

*For better security, credentials should be provided via environment variables.*

- Windows (PowerShell):

$env:PHISHSIM_ADMIN_USER="your_user"
$env:PHISHSIM_ADMIN_PASS="strong_password"
$env:PHISHSIM_SECRET_KEY="random_secret_key"
python app.py


- Linux / macOS:

export PHISHSIM_ADMIN_USER="your_user"
export PHISHSIM_ADMIN_PASS="strong_password"
export PHISHSIM_SECRET_KEY="random_secret_key"
python app.py

## 📄 Targets CSV Format
Targets must be uploaded using a CSV file.

- Required column:
email

- Optional column:
name

Example:
name,
email
Alice,
alice@example.com
Bob,
bob@example.com
Charlie,
charlie@example.com

## 🧪 Usage Workflow

1. Login
Access the dashboard using the admin credentials.

2. Create a Campaign
Provide:
-Campaign name

-Description

-Email subject

-HTML email content

-Example HTML template:
<h3>Hello,</h3>
<p>Please review the information below.</p>
<p><a href="#">Access now</a></p>

3. Upload Targets

Upload the CSV file to generate unique tracking links for each target.

4. Simulate Clicks

Copy a tracking URL

Open it in an incognito/private window

An educational landing page will confirm the simulation

5. Review Metrics

The dashboard displays:

Total targets

Total clicks

Click rate

6. Export Campaign Report

Use the export option to download a CSV report containing:

Targets

Click counts

Tracking URLs

## 📊 Metrics Explanation

Total Clicks
Total number of recorded click events.

Click Rate
Percentage of targets who clicked at least once.

*This reflects real-world security awareness metrics, where repeated clicks by the same user are tracked separately.*

## 🛡️ Security & Ethical Considerations

- No credential harvesting
- No password or sensitive data collection
- No real email sending
- Random, non-guessable tracking tokens
- Intended strictly for authorized awareness simulations

## 🧠 What This Project Demonstrates

- Secure Flask backend development
- SQLite schema design and migrations
- CSV validation and parsing
- Token-based tracking mechanisms
- Security metrics calculation
- Defensive error handling and logging

## 🗺️ Roadmap
- Separate unique click rate vs total clicks in UI
- Optional SMTP email sending (safe / opt-in mode)
- Campaign-specific educational landing pages
- Docker support
- Role-Based Access Control (RBAC)

## 📜 License

*This project is released for educational purposes only.
Use responsibly and ethically.*

## 👤 Author

**Matheus Costa Silva**

Cybersecurity enthusiast with a strong focus on **security awareness**, **defensive security**, and **secure backend development**.  
This project was created as part of a personal portfolio to demonstrate practical skills in **Python**, **Flask**, and **cybersecurity education**.

GitHub: https://github.com/math101101
