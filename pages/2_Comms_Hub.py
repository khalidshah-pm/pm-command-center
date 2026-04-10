import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.comms_hub import generate_comms_outputs
from utils.builders import build_pptx, build_docx

st.set_page_config(
    page_title="Comms Hub — PM Command Center",
    page_icon="📣",
    layout="wide"
)

st.markdown("""
<style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .stTabs [data-baseweb="tab"] { font-size: 15px; font-weight: 500; padding: 10px 20px; }
    .stDownloadButton button { width: 100%; margin-top: 0.5rem; }
    .stExpander { border: 1px solid #e0e0e0; border-radius: 8px; margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)

st.title("📣 Comms Hub")
st.caption(
    "Stakeholder emails, a downloadable PowerPoint deck, and a formal Word status report — "
    "all generated from your project notes in one click."
)
st.divider()

with st.form("comms_form", clear_on_submit=False):
    col1, col2 = st.columns(2)

    with col1:
        project_name = st.text_input("Project Name *", placeholder="e.g. Acme Corp — Digital Transformation")
        client       = st.text_input("Client / Stakeholder Group", placeholder="e.g. Acme Corp")
        period       = st.text_input("Reporting Period", placeholder="e.g. April 2026 / Q2 2026")
        status       = st.selectbox("Overall Assessment", ["Green — On Track", "Amber — At Risk", "Red — Critical"])
        budget       = st.text_input("Budget Status", placeholder="e.g. On budget / 3% over")

    with col2:
        accomplishments = st.text_area(
            "What happened this period? *",
            placeholder="Key deliverables, milestones reached, decisions made.\n\nExample:\n- Phase 2 design signed off by client\n- Integration testing completed ahead of schedule",
            height=130
        )
        upcoming = st.text_area(
            "Upcoming milestones & deadlines",
            placeholder="Example:\n- UAT begins Apr 14\n- Go-live Apr 28\n- Steering committee Apr 17",
            height=95
        )
        risks = st.text_area(
            "Risks & Issues",
            placeholder="Example:\n- Data migration dependency on client IT team — at risk of delay\n- Budget approval for Phase 3 still outstanding",
            height=95
        )

    context = st.text_area(
        "Additional Context (optional — helps the agent write more accurately)",
        placeholder="Background on the project, client relationship, recent decisions, political sensitivities, or anything else the agent should know.",
        height=80
    )

    submitted = st.form_submit_button(
        "Generate Emails + PowerPoint + Word Document",
        type="primary",
        use_container_width=True
    )

if submitted:
    if not project_name or not accomplishments:
        st.error("Please fill in at least the Project Name and what happened this period.")
    else:
        with st.spinner("Agent working — generating communications and building files..."):
            data = {
                "project_name": project_name, "client": client, "period": period,
                "status": status, "accomplishments": accomplishments,
                "upcoming": upcoming, "risks": risks,
                "budget": budget, "context": context
            }
            try:
                results = generate_comms_outputs(data)

                slide_content = results.get("slide_content", {})
                doc_content   = results.get("document_content", {})
                emails        = results.get("emails", {})

                overall = slide_content.get("overall_status", "Amber")
                s_icons = {"Green": "🟢", "Amber": "🟡", "Red": "🔴"}
                st.success(f"{s_icons.get(overall, '🟡')} **{project_name}** — {overall} | {slide_content.get('exec_summary', '')[:100]}...")
                st.divider()

                tab1, tab2, tab3 = st.tabs([
                    "📧 Email Drafts",
                    "📊 PowerPoint Deck",
                    "📄 Word Document"
                ])

                # ── Tab 1: Email Drafts ───────────────────
                with tab1:
                    st.subheader("Five Email Drafts — Ready to Send")
                    st.caption("Copy the version you need. Each is calibrated to its specific scenario.")
                    st.divider()

                    email_configs = [
                        ("status_update",      "📋 Regular Status Update",     "Your standard weekly/monthly update to stakeholders."),
                        ("delay_notice",       "⏱️ Delay / Timeline Update",   "Professional delay notification — honest, solution-focused."),
                        ("milestone_achieved", "🏆 Milestone Achieved",         "Celebrate a delivery while setting up what comes next."),
                        ("change_request",     "🔄 Change Request",             "Formal request for scope, timeline, or budget change approval."),
                        ("escalation",         "🚨 Escalation Notice",          "Urgent escalation that needs leadership action."),
                    ]

                    for key, label, desc in email_configs:
                        email = emails.get(key, {})
                        with st.expander(label, expanded=(key == "status_update")):
                            st.caption(desc)
                            if email:
                                st.markdown(f"**Subject:** {email.get('subject', '')}")
                                st.divider()
                                st.write(email.get("body", ""))
                                st.code(
                                    f"Subject: {email.get('subject', '')}\n\n{email.get('body', '')}",
                                    language=None
                                )

                    # Download all emails as one file
                    all_emails_txt = ""
                    for key, label, _ in email_configs:
                        email = emails.get(key, {})
                        all_emails_txt += (
                            f"{'='*60}\n{label.upper()}\n{'='*60}\n"
                            f"Subject: {email.get('subject', '')}\n\n"
                            f"{email.get('body', '')}\n\n\n"
                        )

                    st.download_button(
                        "Download All 5 Email Drafts (.txt)",
                        all_emails_txt,
                        file_name=f"email_drafts_{project_name.replace(' ', '_')}.txt",
                        use_container_width=True
                    )

                # ── Tab 2: PowerPoint Deck ────────────────
                with tab2:
                    st.subheader("Project Update Deck")
                    st.caption(
                        "A full PowerPoint presentation generated from your project data. "
                        "6 slides — title, executive summary, progress, risks, milestones & next steps, decisions."
                    )

                    # Preview the slide content
                    with st.expander("Preview slide content before downloading"):
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown("**Slide 1 — Title**")
                            st.write(f"• {slide_content.get('project_name', project_name)}")
                            st.write(f"• {slide_content.get('reporting_period', period)}")
                            st.write(f"• Status: {slide_content.get('overall_status', 'Amber')}")
                            st.markdown("**Slide 2 — Executive Summary**")
                            st.write(slide_content.get("exec_summary", ""))
                            st.markdown("**Slide 3 — Progress**")
                            for a in slide_content.get("accomplishments", []):
                                st.write(f"• {a}")
                        with c2:
                            st.markdown("**Slide 4 — Risks**")
                            for r in slide_content.get("risks", []):
                                st.write(f"• [{r.get('severity','')}] {r.get('risk','')}")
                            st.markdown("**Slide 5 — Milestones & Next Steps**")
                            for m in slide_content.get("milestones", []):
                                st.write(f"• {m.get('name','')} — {m.get('date','')} ({m.get('status','')})")
                            decs = slide_content.get("decisions_needed", [])
                            if decs:
                                st.markdown("**Slide 6 — Decisions Needed**")
                                for d in decs:
                                    st.write(f"⚠️ {d}")

                    # Build and offer download
                    try:
                        pptx_bytes = build_pptx(data, slide_content)
                        st.download_button(
                            "Download PowerPoint Deck (.pptx)",
                            data=pptx_bytes,
                            file_name=f"{project_name.replace(' ', '_')}_Update.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            use_container_width=True
                        )
                        st.success("PowerPoint ready. Click above to download.")
                    except Exception as e:
                        st.error(f"PowerPoint generation failed: {str(e)}")
                        st.caption("Make sure python-pptx is installed: `pip install python-pptx`")

                # ── Tab 3: Word Document ──────────────────
                with tab3:
                    st.subheader("Formal Project Status Report")
                    st.caption(
                        "A professional Word document with cover summary table, "
                        "four narrative sections, and appendices. Ready for governance submissions."
                    )

                    with st.expander("Preview document content before downloading"):
                        for section, key in [
                            ("Executive Summary",   "executive_summary"),
                            ("Progress Narrative",  "progress_narrative"),
                            ("Risks Narrative",     "risks_narrative"),
                            ("Next Period Plan",    "next_period_plan"),
                        ]:
                            st.markdown(f"**{section}**")
                            st.write(doc_content.get(key, ""))
                            st.divider()

                    try:
                        docx_bytes = build_docx(data, doc_content, slide_content)
                        st.download_button(
                            "Download Word Document (.docx)",
                            data=docx_bytes,
                            file_name=f"{project_name.replace(' ', '_')}_Status_Report.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True
                        )
                        st.success("Word document ready. Click above to download.")
                    except Exception as e:
                        st.error(f"Word document generation failed: {str(e)}")
                        st.caption("Make sure python-docx is installed: `pip install python-docx`")

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")
                st.caption("Check that your GOOGLE_API_KEY is set in your .env file.")

st.divider()
st.caption("PM Command Center · Built by KhalidShah Virani · Powered by Google Gemini (free)")
