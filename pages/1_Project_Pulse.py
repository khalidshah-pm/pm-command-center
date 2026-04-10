import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.project_pulse import generate_pm_outputs

st.set_page_config(
    page_title="Project Pulse — PM Command Center",
    page_icon="📋",
    layout="wide"
)

st.markdown("""
<style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .stTabs [data-baseweb="tab"] { font-size: 15px; font-weight: 500; padding: 10px 20px; }
    .stDownloadButton button { width: 100%; margin-top: 1rem; }
</style>
""", unsafe_allow_html=True)

st.title("📋 Project Pulse")
st.caption("Paste your raw project notes. Get a status report, action items, stakeholder communications, and an executive briefing — instantly.")
st.divider()

with st.form("pulse_form", clear_on_submit=False):
    col1, col2 = st.columns(2)

    with col1:
        project_name = st.text_input("Project Name *", placeholder="e.g. Acme Corp — ERP Implementation Phase 2")
        client       = st.text_input("Client / Stakeholder Group", placeholder="e.g. Acme Corp")
        period       = st.text_input("Reporting Period", placeholder="e.g. Week of Apr 7–11, 2026")
        status       = st.selectbox("Your Overall Assessment", ["Green — On Track", "Amber — At Risk", "Red — Critical"])
        budget       = st.text_input("Budget Status", placeholder="e.g. On budget / 5% over due to scope change")

    with col2:
        accomplishments = st.text_area(
            "What happened this period? *",
            placeholder="What was completed, delivered, or progressed?\n\nExample:\n- Completed UAT sign-off with client\n- Resolved integration issue with legacy system",
            height=140
        )
        upcoming = st.text_area(
            "Upcoming milestones & deadlines",
            placeholder="What is due next? Critical dates?\n\nExample:\n- Go-live scheduled Apr 25\n- Exec steering committee Apr 18",
            height=100
        )
        risks = st.text_area(
            "Risks & Issues",
            placeholder="What is at risk? Any blockers?\n\nExample:\n- Vendor delivery delayed by 1 week\n- Client approval still pending for Phase 3 SOW",
            height=100
        )

    meeting_notes = st.text_area(
        "Meeting Notes — paste raw notes to extract action items (optional)",
        placeholder="Paste your rough meeting notes here. The agent will extract action items, owners, and due dates.\n\nExample:\nJohn to follow up with vendor by Friday. Sarah will prepare the demo environment before Tuesday.",
        height=120
    )

    submitted = st.form_submit_button("Generate All Outputs", type="primary", use_container_width=True)

if submitted:
    if not project_name or not accomplishments:
        st.error("Please fill in at least the Project Name and what happened this period.")
    else:
        with st.spinner("Agent working..."):
            data = {
                "project_name": project_name, "client": client, "period": period,
                "status": status, "accomplishments": accomplishments,
                "upcoming": upcoming, "risks": risks,
                "meeting_notes": meeting_notes, "budget": budget
            }
            try:
                results = generate_pm_outputs(data)

                health  = results.get("exec_briefing", {}).get("project_health", "On Track")
                headline = results.get("exec_briefing", {}).get("headline", "")
                icons   = {"On Track": "🟢", "At Risk": "🟡", "Critical": "🔴"}
                icon    = icons.get(health, "🟡")

                st.success(f"{icon} **{project_name}** — {health} | {headline}")
                st.divider()

                tab1, tab2, tab3, tab4 = st.tabs([
                    "📋 Status Report", "✅ Action Items",
                    "📣 Stakeholder Comms", "📊 Exec Briefing"
                ])

                # ── Tab 1: Status Report ──────────────────
                with tab1:
                    sr      = results.get("status_report", {})
                    overall = sr.get("overall_status", "Amber")
                    s_icon  = {"Green": "🟢", "Amber": "🟡", "Red": "🔴"}.get(overall, "🟡")

                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.subheader("Executive Summary")
                        st.write(sr.get("summary", ""))
                    with c2:
                        st.metric("Status", f"{s_icon} {overall}")
                        st.caption(sr.get("status_reason", ""))

                    st.divider()
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.subheader("This Period")
                        for i in sr.get("accomplishments", []):
                            st.write(f"• {i}")
                    with c2:
                        st.subheader("Risks & Issues")
                        items = sr.get("risks_issues", [])
                        for i in (items if items else ["None identified"]):
                            st.write(f"• {i}")
                    with c3:
                        st.subheader("Coming Up")
                        for i in sr.get("upcoming", []):
                            st.write(f"• {i}")

                    report_txt = (
                        f"STATUS REPORT — {project_name}\nPeriod: {period}\n"
                        f"Status: {overall} — {sr.get('status_reason', '')}\n\n"
                        f"SUMMARY\n{sr.get('summary', '')}\n\n"
                        f"ACCOMPLISHMENTS\n" + "\n".join(f"• {i}" for i in sr.get("accomplishments", [])) +
                        f"\n\nRISKS & ISSUES\n" + "\n".join(f"• {i}" for i in sr.get("risks_issues", [])) +
                        f"\n\nUPCOMING\n" + "\n".join(f"• {i}" for i in sr.get("upcoming", []))
                    )
                    st.download_button("Download Status Report (.txt)", report_txt,
                                       f"status_report_{project_name.replace(' ', '_')}.txt",
                                       use_container_width=True)

                # ── Tab 2: Action Items ───────────────────
                with tab2:
                    items = results.get("action_items", [])
                    if items:
                        st.subheader(f"{len(items)} Action Items Identified")
                        order = {"High": 0, "Medium": 1, "Low": 2}
                        sorted_items = sorted(items, key=lambda x: order.get(x.get("priority", "Medium"), 1))
                        p_icons = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                        st.markdown(
                            "| # | Action | Owner | Due | Priority |\n|---|--------|-------|-----|----------|\n" +
                            "\n".join(
                                f"| {i+1} | {x.get('action','')} | {x.get('owner','TBD')} "
                                f"| {x.get('due_date','TBD')} "
                                f"| {p_icons.get(x.get('priority','Medium'),'🟡')} {x.get('priority','Medium')} |"
                                for i, x in enumerate(sorted_items)
                            )
                        )
                        txt = f"ACTION ITEMS — {project_name}\n\n"
                        for i, x in enumerate(sorted_items, 1):
                            txt += f"{i}. {x.get('action','')}\n   Owner: {x.get('owner','TBD')} | Due: {x.get('due_date','TBD')} | Priority: {x.get('priority','Medium')}\n\n"
                        st.download_button("Download Action Items (.txt)", txt,
                                           f"action_items_{project_name.replace(' ', '_')}.txt",
                                           use_container_width=True)
                    else:
                        st.info("Add meeting notes in the form above to extract action items.")

                # ── Tab 3: Stakeholder Comms ──────────────
                with tab3:
                    comms = results.get("stakeholder_comms", {})
                    st.subheader("Three audiences. Three versions.")
                    st.caption("Same data — calibrated to what each audience needs to hear.")
                    st.divider()
                    for label, key, desc in [
                        ("🎯 Executive Sponsor", "executive_sponsor", "Strategic, decision-focused."),
                        ("🤝 Client",             "client",             "Professional, transparent."),
                        ("⚙️ Internal Team",      "internal_team",      "Direct, practical, action-oriented."),
                    ]:
                        with st.expander(label, expanded=(key == "executive_sponsor")):
                            st.caption(desc)
                            t = comms.get(key, "")
                            st.write(t)
                            st.code(t, language=None)

                # ── Tab 4: Exec Briefing ──────────────────
                with tab4:
                    eb = results.get("exec_briefing", {})
                    st.subheader("Steering Committee Briefing")
                    st.markdown(f"### {eb.get('headline', '')}")
                    st.divider()
                    c1, c2 = st.columns(2)
                    with c1:
                        st.subheader("Key Points")
                        for p in eb.get("key_points", []):
                            st.write(f"• {p}")
                    with c2:
                        decs = eb.get("decisions_needed", [])
                        st.subheader("Decisions Needed")
                        if decs:
                            for d in decs:
                                st.warning(f"⚠️ {d}")
                        else:
                            st.success("No decisions required this period.")
                    st.divider()
                    st.info(f"**Bottom Line:** {eb.get('bottom_line', '')}")

                    briefing_txt = (
                        f"EXECUTIVE BRIEFING — {project_name}\nPeriod: {period}\n"
                        f"Health: {eb.get('project_health', '')}\n\n"
                        f"{eb.get('headline', '')}\n\n"
                        f"KEY POINTS\n" + "\n".join(f"• {p}" for p in eb.get("key_points", [])) +
                        f"\n\nDECISIONS NEEDED\n" +
                        ("\n".join(f"• {d}" for d in eb.get("decisions_needed", [])) or "• None this period") +
                        f"\n\nBOTTOM LINE\n{eb.get('bottom_line', '')}"
                    )
                    st.download_button("Download Exec Briefing (.txt)", briefing_txt,
                                       f"exec_briefing_{project_name.replace(' ', '_')}.txt",
                                       use_container_width=True)

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")
                st.caption("Check that your GOOGLE_API_KEY is set in your .env file.")

st.divider()
st.caption("PM Command Center · Built by KhalidShah Virani · Powered by Google Gemini (free)")
