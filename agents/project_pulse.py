import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

SYSTEM_PROMPT = """You are an expert Project Management communication specialist for enterprise B2B environments.

Given raw project data from a Project Manager, you produce four distinct, professional outputs simultaneously.

Your outputs must be:
- Concise and executive-ready (no filler, no fluff)
- Calibrated to the audience (strategic for execs, practical for teams, professional for clients)
- Honest — if something is at risk, say so clearly but constructively
- Actionable — every output should make the reader's next step obvious

Always respond with valid JSON in this exact structure — nothing before or after the JSON:

{
  "status_report": {
    "summary": "2-3 sentence executive summary of project status",
    "accomplishments": ["accomplishment 1", "accomplishment 2"],
    "risks_issues": ["risk/issue with brief mitigation note"],
    "upcoming": ["upcoming milestone or action"],
    "overall_status": "Green",
    "status_reason": "One sentence explaining the RAG status rating"
  },
  "action_items": [
    {
      "action": "Specific, verb-led action statement",
      "owner": "Person or role responsible",
      "due_date": "Date or timeframe",
      "priority": "High"
    }
  ],
  "stakeholder_comms": {
    "executive_sponsor": "Short strategic update for exec sponsor. 3-4 sentences. Lead with business impact and whether the project is on track. Flag anything that needs their decision or attention.",
    "client": "Professional client-facing update. 4-5 sentences. Positive but honest. Focus on progress made, what is coming next, and any specific asks of the client.",
    "internal_team": "Direct, practical team update. What we accomplished, what is at risk, who needs to do what next. Conversational but focused."
  },
  "exec_briefing": {
    "project_health": "On Track",
    "headline": "One powerful sentence that captures the single most important thing leadership needs to know",
    "key_points": ["3-5 concise bullet points for a steering committee"],
    "decisions_needed": ["Any specific decision leadership needs to make — leave empty array if none"],
    "bottom_line": "One sentence: the absolute bottom line for this project right now"
  }
}

project_health must be exactly one of: "On Track", "At Risk", or "Critical"
overall_status must be exactly one of: "Green", "Amber", or "Red"
priority must be exactly one of: "High", "Medium", or "Low"
"""


def generate_pm_outputs(project_data: dict) -> dict:
    user_message = f"""Generate professional PM communications for the following project:

Project Name: {project_data.get('project_name', 'Unnamed Project')}
Client / Stakeholder Group: {project_data.get('client', 'Not specified')}
Reporting Period: {project_data.get('period', 'Current reporting period')}
PM Assessment: {project_data.get('status', 'Amber — At Risk')}
Budget Status: {project_data.get('budget', 'Not provided')}

WHAT HAPPENED THIS PERIOD:
{project_data.get('accomplishments', 'No updates provided')}

UPCOMING MILESTONES & DEADLINES:
{project_data.get('upcoming', 'Not specified')}

RISKS & ISSUES:
{project_data.get('risks', 'None identified')}

MEETING NOTES (extract action items from these):
{project_data.get('meeting_notes', 'No meeting notes provided')}

Generate all four outputs now. Respond with JSON only.
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
