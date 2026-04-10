# PM Command Center

> AI-powered tools for enterprise B2B project managers. Free, open source, no credit card required.

---

## The Problem

Enterprise B2B project managers spend hours every week on communication work that creates no value:

- Manually compiling status reports from scattered notes, emails, and Jira
- Rewriting the same update three times for different audiences
- Building PowerPoint decks for steering committees from scratch
- Chasing action items that got buried in meeting notes

PM Command Center automates all of it. You provide the raw project data. The AI generates everything else.

---

## Modules

### 📋 Project Pulse — Weekly Reporting Agent

Paste your raw notes once. Get four outputs instantly:

| Output | What you get |
|--------|-------------|
| **Status Report** | Executive summary, RAG status, accomplishments, risks, upcoming milestones |
| **Action Items** | Extracted from meeting notes with owner, due date, and priority |
| **Stakeholder Comms** | Three versions: Executive Sponsor, Client, Internal Team |
| **Exec Briefing** | Steering committee summary — key points, decisions needed, bottom line |

---

### 📣 Comms Hub — Communication & Document Automation

One set of project inputs. Three types of output:

| Output | What you get |
|--------|-------------|
| **Email Drafts** | Five ready-to-send emails: status update, delay notice, milestone achieved, change request, escalation |
| **PowerPoint Deck** | A downloadable `.pptx` file — 6-slide project update presentation |
| **Word Document** | A downloadable `.docx` — formal project status report for governance submissions |

---

## Tech Stack

- **[Streamlit](https://streamlit.io)** — web interface, runs in your browser
- **[Google Gemini API](https://aistudio.google.com)** — AI that generates all content (free tier)
- **[python-pptx](https://python-pptx.readthedocs.io)** — builds the PowerPoint files
- **[python-docx](https://python-docx.readthedocs.io)** — builds the Word documents
- **Python** — glue

---

## Setup — Free, No Credit Card

### 1. Get a free Google API key (30 seconds)

Go to **[aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)** and click **Create API Key**.
Just a Google account — no payment, no trial.

**Free tier:** 1,500 requests/day · 1 million tokens/day

### 2. Clone and install

```bash
git clone https://github.com/khalidshah-pm/pm-command-center.git
cd pm-command-center
pip install -r requirements.txt
```

### 3. Add your API key

```bash
cp .env.example .env
```

Open `.env` and paste your key from Google AI Studio.

### 4. Run

```bash
streamlit run Home.py
```

Opens at `http://localhost:8501`.

---

## Project Structure

```
pm-command-center/
├── Home.py                     # Landing page with module navigation
├── pages/
│   ├── 1_Project_Pulse.py      # Module 1: Weekly reporting agent
│   └── 2_Comms_Hub.py          # Module 2: Communication & document automation
├── agents/
│   ├── project_pulse.py        # AI agent logic for Project Pulse
│   └── comms_hub.py            # AI agent logic for Comms Hub
├── utils/
│   └── builders.py             # PowerPoint and Word document builders
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Why I Built This

I'm a Product Manager with 8+ years in enterprise B2B. Status reporting, stakeholder communication, and governance documentation are universal PM pain points — high-frequency, low-value work that keeps smart people from doing the actual job.

PM Command Center is built from real PM experience. The outputs are structured around what enterprise stakeholders actually need to see, not generic templates.

---

## Roadmap

- [ ] Module 3: Risk & Change Manager — AI-powered risk register and change impact analysis
- [ ] Module 4: Meeting Intelligence — upload a transcript, get full meeting intelligence
- [ ] Streamlit Cloud deployment (one-click share with your team)
- [ ] Export to PDF

---

## About

**KhalidShah Virani** — Associate Product Manager at Ecolab | Chemical Engineering + MBA | Building AI tools for enterprise PM and product teams.

- [LinkedIn](https://linkedin.com/in/your-profile)
- [GitHub](https://github.com/khalidshah-pm)

---

## License

MIT — use it, fork it, build on it.
