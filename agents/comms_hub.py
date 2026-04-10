import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

SYSTEM_PROMPT = """You are a senior enterprise B2B project communications specialist.

Given raw project data, you generate three types of output:
1. Five professional email drafts for different stakeholder scenarios
2. Structured slide content for a project update PowerPoint deck
3. Narrative content for a formal project status document

Rules:
- Emails must be professional, appropriately concise, and ready to send with minimal editing
- Slide content must be punchy — bullet points under 12 words each
- Document narratives should be formal but readable — one solid paragraph each
- Be honest about risks without being alarmist
- overall_status must be exactly: "Green", "Amber", or "Red"
- milestone status must be exactly: "Complete", "On Track", or "At Risk"
- risk severity must be exactly: "High", "Medium", or "Low"

Respond with valid JSON only — no text before or after:

{
  "emails": {
    "status_update": {
      "subject": "Project Status Update: [Project Name] — [Period]",
      "body": "Full professional email body, 4-6 paragraphs. Include greeting, project summary, key updates, risks if any, next steps, and sign-off."
    },
    "delay_notice": {
      "subject": "Project Timeline Update: [Project Name]",
      "body": "Professional delay notification. Acknowledge the delay, explain root cause briefly, state revised timeline, outline mitigation steps, and maintain confidence."
    },
    "milestone_achieved": {
      "subject": "Milestone Achieved: [Milestone Name] — [Project Name]",
      "body": "Celebratory but professional. Acknowledge the milestone, thank contributors, state business impact, and set up what comes next."
    },
    "change_request": {
      "subject": "Change Request for Approval: [Project Name]",
      "body": "Formal change request email. State the change clearly, explain why it is needed, describe impact on scope/timeline/budget, and request approval."
    },
    "escalation": {
      "subject": "Escalation Required: [Project Name] — [Issue]",
      "body": "Urgent but professional escalation. State the issue clearly, explain business impact, describe what has already been tried, and state what decision or action is needed from leadership."
    }
  },
  "slide_content": {
    "project_name": "Project name for slides",
    "reporting_period": "Reporting period",
    "overall_status": "Green",
    "exec_summary": "2-3 sentence executive summary for the slide deck",
    "key_metrics": [
      {"label": "Schedule", "value": "On Track"},
      {"label": "Budget", "value": "On Budget"},
      {"label": "Scope", "value": "Controlled"},
      {"label": "Resources", "value": "Fully Staffed"}
    ],
    "accomplishments": ["Short accomplishment bullet 1", "Short accomplishment bullet 2"],
    "risks": [
      {"risk": "Brief risk description", "severity": "High", "mitigation": "Brief mitigation action"}
    ],
    "milestones": [
      {"name": "Milestone name", "date": "Date or timeframe", "status": "Complete"}
    ],
    "next_steps": ["Next step 1", "Next step 2"],
    "decisions_needed": ["Decision needed from leadership — leave empty array if none"]
  },
  "document_content": {
    "executive_summary": "One formal paragraph summarising the overall project status, key achievements, and outlook.",
    "progress_narrative": "One formal paragraph describing what was accomplished this period in detail.",
    "risks_narrative": "One formal paragraph describing current risks, their potential impact, and mitigation plans.",
    "next_period_plan": "One formal paragraph outlining what will happen next period and what success looks like."
  }
}
"""


def generate_comms_outputs(project_data: dict) -> dict:
    """
    Takes raw project data and returns email drafts, slide content, and document content.
    Uses Google Gemini — free tier, no credit card required.
    """
    user_message = f"""Generate all communications for the following project:

Project Name: {project_data.get('project_name', 'Unnamed Project')}
Client / Stakeholder Group: {project_data.get('client', 'Not specified')}
Reporting Period: {project_data.get('period', 'Current period')}
PM Assessment: {project_data.get('status', 'Amber — At Risk')}
Budget Status: {project_data.get('budget', 'Not provided')}

WHAT HAPPENED THIS PERIOD:
{project_data.get('accomplishments', 'No updates provided')}

UPCOMING MILESTONES & DEADLINES:
{project_data.get('upcoming', 'Not specified')}

RISKS & ISSUES:
{project_data.get('risks', 'None identified')}

KEY CONTEXT / BACKGROUND:
{project_data.get('context', 'No additional context provided')}

Generate all outputs now. Respond with JSON only.
"""

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )

    response = model.generate_content(user_message)
    response_text = response.text.strip()

    if response_text.startswith("```json"):
        response_text = response_text[7:]
    if response_text.startswith("```"):
        response_text = response_text[3:]
    if response_text.endswith("```"):
        response_text = response_text[:-3]

    return json.loads(response_text.strip())
