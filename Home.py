import streamlit as st

st.set_page_config(
    page_title="PM Command Center",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .block-container { padding-top: 3rem; }
    .module-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e9ecef;
        height: 100%;
    }
    .module-card h3 { margin-top: 0; }
</style>
""", unsafe_allow_html=True)

st.title("PM Command Center")
st.caption("AI-powered tools for enterprise B2B project managers — free, no credit card required.")
st.divider()

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
### 📋 Project Pulse

Your weekly reporting agent. Paste your raw notes, get four polished outputs instantly.

**What it generates:**
- Weekly status report (RAG status, summary, accomplishments, risks)
- Action items extracted from meeting notes — with owner, due date, and priority
- Three stakeholder communications: Executive Sponsor, Client, Internal Team
- Executive briefing ready for your steering committee

**Best for:** Weekly reporting cycles, steering committee prep, status updates

---
""")
    st.page_link("pages/1_Project_Pulse.py", label="Open Project Pulse →", icon="📋")

with col2:
    st.markdown("""
### 📣 Comms Hub

Your stakeholder communication and document generation agent. One input, multiple professional outputs — including downloadable files.

**What it generates:**
- Five email drafts: status update, delay notice, milestone achieved, change request, escalation
- Downloadable PowerPoint deck — a full project update presentation
- Downloadable Word document — a formal project status report

**Best for:** Client communications, stakeholder updates, governance reporting, executive presentations

---
""")
    st.page_link("pages/2_Comms_Hub.py", label="Open Comms Hub →", icon="📣")

st.divider()

st.markdown("""
<div style="text-align: center; color: #6c757d; font-size: 0.85rem; padding: 1rem 0;">
    Built by <a href="https://github.com/virankh" target="_blank">KhalidShah Virani</a> &nbsp;·&nbsp;
    Powered by Google Gemini (free tier) &nbsp;·&nbsp;
    <a href="https://github.com/virankh/pm-command-center" target="_blank">View on GitHub</a>
</div>
""", unsafe_allow_html=True)
