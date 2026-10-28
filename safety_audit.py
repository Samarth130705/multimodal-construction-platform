"""
Tab 1: Site Safety & PPE Audit Module (Epic 2)
Analyzes worker PPE compliance and site physical hazards under OSHA 1926 & IS 456 standards.
"""
import json
from typing import Optional, Tuple, Dict, Any

try:
    import streamlit as st
except ImportError:
    st = None

from .gemini_client import run_gemini_vision
from .sample_assets import get_mock_safety_data

SAFETY_AUDIT_PROMPT = """
You are an accredited Senior Construction Safety Auditor and OSHA / Bureau of Indian Standards (IS 456 / IS 2925) Compliance Inspector.
Inspect this construction site image with high precision. Analyze worker PPE compliance and identify environmental and structural hazards.

Output MUST be a strict, valid JSON object with the exact following schema:
{
  "safety_score": <integer from 0 to 100 based on overall compliance and hazard severity>,
  "overall_status": "<'Compliant' | 'Warning - Action Required' | 'Critical Non-Compliance'>",
  "compliance_summary": "<concise 2-sentence executive summary>",
  "workers_detected_count": <integer count of workers visible>,
  "ppe_detection": [
    {
      "item": "Hard Hats / Safety Helmets",
      "status": "<'Compliant' | 'Partial' | 'Non-Compliant'>",
      "detected_count": <integer>,
      "expected_count": <integer>,
      "compliance_rate": <integer 0-100>,
      "standard": "OSHA 1926.100 / IS 2925",
      "notes": "<specific observation about helmet usage, chinstraps, conditions>"
    },
    {
      "item": "High-Visibility Safety Vests",
      "status": "<'Compliant' | 'Partial' | 'Non-Compliant'>",
      "detected_count": <integer>,
      "expected_count": <integer>,
      "compliance_rate": <integer 0-100>,
      "standard": "OSHA 1926.201 / EN ISO 20471",
      "notes": "<observation on retroreflective vests, visibility in lighting>"
    },
    {
      "item": "Steel-Toe Protective Footwear",
      "status": "<'Compliant' | 'Partial' | 'Non-Compliant'>",
      "detected_count": <integer>,
      "expected_count": <integer>,
      "compliance_rate": <integer 0-100>,
      "standard": "OSHA 1926.96 / IS 15298",
      "notes": "<observation on work boots, exposed feet, toe caps>"
    },
    {
      "item": "Fall Arrest Harness & Lifelines",
      "status": "<'Compliant' | 'Partial' | 'Non-Compliant'>",
      "detected_count": <integer>,
      "expected_count": <integer>,
      "compliance_rate": <integer 0-100>,
      "standard": "OSHA 1926.502 / IS 3521",
      "notes": "<observation on elevated lanyard anchors, harnesses, static lines>"
    },
    {
      "item": "Eye, Face & Respiratory Protection",
      "status": "<'Compliant' | 'Partial' | 'Non-Compliant'>",
      "detected_count": <integer>,
      "expected_count": <integer>,
      "compliance_rate": <integer 0-100>,
      "standard": "OSHA 1926.102 / IS 8521",
      "notes": "<observation on goggles, face shields, dust respirators>"
    }
  ],
  "site_hazards": [
    {
      "hazard": "<hazard title>",
      "severity": "<'Low' | 'Medium' | 'High' | 'Critical'>",
      "location_zone": "<approximate location on site or in frame>",
      "regulatory_violation": "<OSHA and/or Indian Standard clause>",
      "corrective_remedy": "<actionable, immediate engineering and managerial control remedy>"
    }
  ]
}
Return only JSON. Do not include markdown formatting or commentary outside the JSON block.
"""

def execute_safety_audit(
    image_bytes: bytes, 
    mime_type: str = "image/jpeg", 
    api_key: Optional[str] = None, 
    sample_id: str = "sample_1"
) -> Tuple[Dict[str, Any], bool, str]:
    """
    Runs PPE audit via Gemini Multimodal API with fallback to mock data.
    """
    if api_key and len(api_key.strip()) > 10:
        is_live, parsed, msg = run_gemini_vision(SAFETY_AUDIT_PROMPT, image_bytes, mime_type, api_key)
        if is_live and parsed:
            # Validate required keys
            if "safety_score" in parsed and "ppe_detection" in parsed:
                return parsed, True, msg
    
    # Fallback to realistic mock scenario
    mock_data = get_mock_safety_data(sample_id)
    return mock_data, False, "Demonstration Mode Active (High-Fidelity Simulated Analysis)"


def render_safety_audit_view(data: Dict[str, Any], is_live: bool, status_msg: str):
    """
    Renders production-grade safety dashboard with metric cards, status pills, and downloadable JSON.
    """
    score = data.get("safety_score", 0)
    overall_status = data.get("overall_status", "Unknown")
    workers_count = data.get("workers_detected_count", 0)
    hazards = data.get("site_hazards", [])
    ppe_items = data.get("ppe_detection", [])
    summary = data.get("compliance_summary", "")

    # Top Status Pill & Mode Indicator
    mode_color = "#10B981" if is_live else "#F59E0B"
    mode_badge = "🟢 LIVE GEMINI MULTIMODAL INFERENCE" if is_live else "🟡 DEMONSTRATION MODE (SIMULATED TELEMETRY)"
    
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); 
                    padding: 10px 18px; border-radius: 10px; margin-bottom: 20px;">
            <div style="font-weight: 600; color: #E2E8F0; font-size: 0.95rem;">
                Audit Engine: <span style="color: {mode_color};">{mode_badge}</span>
            </div>
            <div style="font-size: 0.85rem; color: #94A3B8;">
                {status_msg}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Big Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    
    # Score color logic
    if score >= 80:
        score_color = "#10B981" # Green
        status_bg = "rgba(16, 185, 129, 0.2)"
        status_border = "#10B981"
    elif score >= 60:
        score_color = "#F59E0B" # Amber
        status_bg = "rgba(245, 158, 11, 0.2)"
        status_border = "#F59E0B"
    else:
        score_color = "#EF4444" # Red
        status_bg = "rgba(239, 68, 68, 0.2)"
        status_border = "#EF4444"

    critical_count = sum(1 for h in hazards if h.get("severity", "").lower() == "critical")

    with m1:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 4px solid {score_color};">
                <div class="metric-label">Safety Compliance Score</div>
                <div class="metric-value" style="color: {score_color};">{score}<span style="font-size:1.2rem; color:#94A3B8;">/100</span></div>
            </div>
            """, 
            unsafe_allow_html=True
        )

    with m2:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 4px solid {status_border};">
                <div class="metric-label">Overall Site Status</div>
                <div style="margin-top: 10px;">
                    <span class="status-pill" style="background: {status_bg}; color: {score_color}; border: 1px solid {status_border};">
                        {overall_status}
                    </span>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )

    with m3:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 4px solid #3B82F6;">
                <div class="metric-label">Operatives in Frame</div>
                <div class="metric-value" style="color: #60A5FA;">{workers_count} <span style="font-size:1rem; color:#94A3B8;">Workers</span></div>
            </div>
            """, 
            unsafe_allow_html=True
        )

    with m4:
        hazard_border = "#EF4444" if critical_count > 0 else "#F59E0B"
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 4px solid {hazard_border};">
                <div class="metric-label">Identified Hazards</div>
                <div class="metric-value" style="color: {hazard_border};">{len(hazards)} <span style="font-size:0.9rem; color:#94A3B8;">({critical_count} Critical)</span></div>
            </div>
            """, 
            unsafe_allow_html=True
        )

    # Executive Summary Card
    if summary:
        st.info(f"📋 **Site Safety Executive Brief:** {summary}")

    st.markdown("---")

    # PPE Inspection Checklist Section
    col_left, col_right = st.columns([1.1, 0.9])

    with col_left:
        st.subheader("🛡️ PPE Compliance Detection Checklist (OSHA & IS 456)")
        for item in ppe_items:
            name = item.get("item", "PPE Item")
            status = item.get("status", "Unknown")
            det = item.get("detected_count", 0)
            exp = item.get("expected_count", workers_count)
            rate = item.get("compliance_rate", 0)
            std = item.get("standard", "")
            notes = item.get("notes", "")

            if status.lower() == "compliant":
                badge_bg = "rgba(16, 185, 129, 0.15)"
                badge_border = "#10B981"
                badge_icon = "✅"
                badge_text = "COMPLIANT"
            elif status.lower() == "partial":
                badge_bg = "rgba(245, 158, 11, 0.15)"
                badge_border = "#F59E0B"
                badge_icon = "⚠️"
                badge_text = "PARTIAL COMPLIANCE"
            else:
                badge_bg = "rgba(239, 68, 68, 0.15)"
                badge_border = "#EF4444"
                badge_icon = "❌"
                badge_text = "NON-COMPLIANT"

            st.markdown(
                f"""
                <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); 
                            border-radius: 8px; padding: 12px 16px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-weight: 600; font-size: 1rem; color: #F1F5F9;">{name}</span>
                        <span style="background: {badge_bg}; color: {badge_border}; border: 1px solid {badge_border}; 
                                    padding: 2px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700;">
                            {badge_icon} {badge_text} ({rate}%)
                        </span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #94A3B8; margin-bottom: 6px;">
                        <span>Standard: <code>{std}</code></span>
                        <span>Detected: <b>{det} / {exp}</b></span>
                    </div>
                    <div style="font-size: 0.85rem; color: #CBD5E1; line-height: 1.4;">
                        {notes}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col_right:
        st.subheader("⚠️ Site Hazards & Corrective Engineering Remedies")
        if not hazards:
            st.success("No critical or elevated site hazards identified in this capture zone.")
        else:
            for idx, hz in enumerate(hazards, 1):
                h_name = hz.get("hazard", f"Hazard #{idx}")
                sev = hz.get("severity", "Medium")
                loc = hz.get("location_zone", "General Site Area")
                vio = hz.get("regulatory_violation", "Safety Regulation")
                rem = hz.get("corrective_remedy", "Take remedial action.")

                if sev.lower() == "critical":
                    s_color = "#EF4444"
                    s_icon = "🛑"
                elif sev.lower() == "high":
                    s_color = "#F97316"
                    s_icon = "🔴"
                elif sev.lower() == "medium":
                    s_color = "#F59E0B"
                    s_icon = "🟠"
                else:
                    s_color = "#3B82F6"
                    s_icon = "🟡"

                with st.expander(f"{s_icon} [{sev.upper()}] {h_name}", expanded=(idx <= 2)):
                    st.markdown(f"**📍 Location Zone:** {loc}")
                    st.markdown(f"**⚖️ Standard Violated:** `{vio}`")
                    st.markdown(
                        f"""
                        <div style="background: rgba(239, 68, 68, 0.08); border-left: 3px solid {s_color}; 
                                    padding: 8px 12px; border-radius: 4px; margin-top: 8px;">
                            <span style="font-weight: 700; color: #F8FAFC;">Corrective Remedy:</span><br/>
                            <span style="color: #E2E8F0; font-size: 0.9rem;">{rem}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    # Downloadable JSON Report & Export
    st.markdown("---")
    down_col1, down_col2 = st.columns([1, 1])
    json_str = json.dumps(data, indent=2)

    with down_col1:
        st.download_button(
            label="📥 Download Structured Audit Report (JSON)",
            data=json_str,
            file_name="site_safety_ppe_audit.json",
            mime="application/json",
            use_container_width=True
        )

    with down_col2:
        # Formatted markdown summary
        md_summary = f"""# CONSTRUCTION SITE SAFETY & PPE AUDIT REPORT
Standard: OSHA 29 CFR 1926 & IS 456:2000
Safety Score: {score}/100 ({overall_status})
Workers Detected: {workers_count}
Identified Hazards: {len(hazards)}

## PPE COMPLIANCE:
"""
        for item in ppe_items:
            md_summary += f"- {item.get('item')}: {item.get('status')} ({item.get('compliance_rate', 0)}%) [{item.get('standard')}]\n"

        md_summary += "\n## REMEDIAL ACTION PLAN:\n"
        for hz in hazards:
            md_summary += f"- [{hz.get('severity')}] {hz.get('hazard')} ({hz.get('location_zone')}): {hz.get('corrective_remedy')}\n"

        st.download_button(
            label="📄 Download Site Action Summary (Markdown)",
            data=md_summary,
            file_name="site_safety_action_plan.md",
            mime="text/markdown",
            use_container_width=True
        )
