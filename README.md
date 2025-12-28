# phish-sim-lab 🎣 (Educational Phishing Simulation)

Toolkit educacional para simular campanhas de phishing **com autorização** (security awareness).
Cria campanhas, importa targets, gera links únicos por alvo, registra cliques e exporta relatório CSV.

> ⚠️ **Uso ético apenas:** não use para fins maliciosos.

---

## Features
- Login admin (local)
- Criar campanha (assunto + HTML do email)
- Upload de targets via CSV (`name,email`)
- Link único por target: `/t/<token>`
- Log de cliques (data/hora, IP, user-agent)
- Dashboard com métricas
- Export CSV: `reports/campaign_report.csv`

---

## Requisitos
- Python 3.11+

---

## Como rodar
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
python app.py
