"""
Tab 2: Crack Diagnostics & Structural Integrity Module (Epic 2)
Forensic AI analysis classifying structural defects, estimating crack widths, and prescribing IS 456 & ACI 224 repairs.
"""
import json
from typing import Optional, Tuple, Dict, Any

try:
    import streamlit as st
except ImportError:
    st = None

from .gemini_client import run_gemini_vision
from .sample_assets import get_mock_crack_data

CRACK_DIAGNOSTICS_PROMPT = """
You are a Principal Forensic Structural Engineer and Concrete Integrity Specialist (IS 456:2000, ACI 224.1R, ICRI 310.1R certified).
Analyze the structural concrete/wall surface photo provided. 

Perform full engineering defect classification and diagnostics.
Output MUST be a strict, valid JSON object with the exact following schema:
{
  "defect_type": "<'Hairline Crack' | 'Settlement Crack' | 'Structural Shear Crack' | 'Thermal Expansion Crack' | 'Concrete Spalling & Rebar Delamination'>",
  "estimated_crack_width_mm": <float estimated width in millimeters>,
  "severity_index": "<'Minor Non-Structural' | 'Moderate Durability Concern' | 'High Engineering Risk' | 'Critical Structural Defect'>",
  "urgency": "<'Immediate Structural Evacuation / Shoring' | 'High Priority (Remediate within 7 days)' | 'Routine Maintenance' | 'Periodic Monitoring (Install crack gauge)'>",
  "structural_element": "<identified element: e.g. RC Girder, Column Capital, Slab Soffit, Masonry Infill>",
  "is_code_reference": "<relevant clause from IS 456:2000, e.g. Clause 35.3.2 or Clause 40>",
  "root_causes": [
    "<detailed engineering root cause 1>",
    "<detailed engineering root cause 2>",
    "<detailed engineering root cause 3>"
  ],
  "engineering_repairs": [
    {
      "step": <integer>,
      "action": "<engineering repair procedure name>",
      "specification": "<detailed technical specification including ASTM/IS materials, psi/MPa pressure, epoxy grade, mortar class>"
    }
  ],
  "risk_assessment": {
    "load_capacity_reduction_pct": <estimated integer percentage 0-100>,
    "water_ingress_risk": "<'None' | 'Moderate' | 'Severe'>",
    "monitoring_frequency": "<recommended inspection cadence>"
  }
}
Return only JSON. Do not include markdown formatting or commentary outside the JSON block.
"""

def execute_crack_diagnostics(
    image_bytes: bytes, 
    mime_type: str = "image/jpeg", 
    api_key: Optional[str] = None, 
    sample_id: str = "sample_1"
) -> Tuple[Dict[str, Any], bool, str]:
    """
    Executes structural crack diagnostics with Gemini Multimodal or mock fallback.
    """
    if api_key and len(api_key.strip()) > 10:
        is_live, parsed, msg = run_gemini_vision(CRACK_DIAGNOSTICS_PROMPT, image_bytes, mime_type, api_key)
        if is_live and parsed:
            if "defect_type" in parsed and "estimated_crack_width_mm" in parsed:
                return parsed, True, msg
                
    mock_data = get_mock_crack_data(sample_id)
    return mock_data, False, "Demonstration Mode Active (High-Fidelity Simulated Structural Telemetry)"


def render_crack_diagnostics_view(data: Dict[str, Any], is_live: bool, status_msg: str):
    """
    Renders the structural defect diagnostic console.
    """
    defect = data.get("defect_type", "Structural Crack")
    width_mm = data.get("estimated_crack_width_mm", 0.0)
    severity = data.get("severity_index", "Under Review")
    urgency = data.get("urgency", "Monitor")
    element = data.get("structural_element", "RC Structural Member")
    code_ref = data.get("is_code_reference", "IS 456:2000")
    causes = data.get("root_causes", [])
    repairs = data.get("engineering_repairs", [])
    risk = data.get("risk_assessment", {})

    # Status Pill & Mode Indicator
    mode_color = "#10B981" if is_live else "#F59E0B"
    mode_badge = "🟢 LIVE FORENSIC VISION INFERENCE" if is_live else "🟡 DEMONSTRATION MODE (STRUCTURAL TELEMETRY)"
    
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); 
                    padding: 10px 18px; border-radius: 10px; margin-bottom: 20px;">
            <div style="font-weight: 600; color: #E2E8F0; font-size: 0.95rem;">
                Diagnostics Engine: <span style="color: {mode_color};">{mode_badge}</span>
            </div>
            <div style="font-size: 0.85rem; color: #94A3B8;">
                {status_msg}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Urgency & Severity Styling
    if "immediate" in urgency.lower() or "critical" in severity.lower():
        urgency_color = "#EF4444"
        urgency_bg = "rgba(239, 68, 68, 0.2)"
    elif "high" in urgency.lower() or "high" in severity.lower():
        urgency_color = "#F97316"
        urgency_bg = "rgba(249, 115, 22, 0.2)"
    else:
        urgency_color = "#10B981"
        urgency_bg = "rgba(16, 185, 129, 0.2)"

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 4px solid #3B82F6;">
                <div class="metric-label">Defect Classification</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #60A5FA; margin-top: 6px; line-height: 1.2;">
                    {defect}
                </div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">Element: {element}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        # IS 456 permissible crack width limit is 0.3mm for mild exposure, 0.2mm for severe
        width_warning = "⚠️ Exceeds IS 456 Permissible Limit (0.3mm)" if width_mm > 0.3 else "✅ Within Serviceability Limit"
        w_color = "#EF4444" if width_mm > 1.5 else ("#F59E0B" if width_mm > 0.3 else "#10B981")
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 4px solid {w_color};">
                <div class="metric-label">Estimated Crack Width</div>
                <div class="metric-value" style="color: {w_color};">{width_mm:.2f} <span style="font-size:1.1rem; color:#94A3B8;">mm</span></div>
                <div style="font-size: 0.72rem; color: #CBD5E1; margin-top: 2px;">{width_warning}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 4px solid {urgency_color};">
                <div class="metric-label">Remediation Urgency</div>
                <div style="margin-top: 8px;">
                    <span class="status-pill" style="background: {urgency_bg}; color: {urgency_color}; border: 1px solid {urgency_color};">
                        {urgency}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        cap_drop = risk.get("load_capacity_reduction_pct", 0)
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 4px solid #8B5CF6;">
                <div class="metric-label">Capacity Impairment</div>
                <div class="metric-value" style="color: #A78BFA;">-{cap_drop}% <span style="font-size:0.9rem; color:#94A3B8;">Shear/Flexure</span></div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 2px;">Code: <code>{code_ref}</code></div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Detailed Root Causes & Recommended Engineering Repairs
    col_causes, col_repairs = st.columns([1, 1.3])

    with col_causes:
        st.subheader("🔬 Forensic Root Cause Analysis")
        st.markdown(f"**Structural Element:** `{element}`")
        st.markdown(f"**Code Benchmark:** `{code_ref}`")
        
        for idx, cause in enumerate(causes, 1):
            st.markdown(
                f"""
                <div style="background: rgba(30, 41, 59, 0.6); border-left: 3px solid #3B82F6; 
                            padding: 10px 14px; border-radius: 6px; margin-bottom: 10px; font-size: 0.9rem; color: #E2E8F0;">
                    <b>{idx}.</b> {cause}
                </div>
                """,
                unsafe_allow_html=True
            )

        # Risk Matrix Card
        st.markdown("#### 📊 Structural Risk Assessment")
        water_risk = risk.get("water_ingress_risk", "Moderate")
        cadence = risk.get("monitoring_frequency", "Weekly")
        st.markdown(
            f"""
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255, 255, 255, 0.08); 
                        padding: 12px 16px; border-radius: 8px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px; font-size: 0.85rem;">
                    <span style="color: #94A3B8;">Water Ingress & Corrosion Risk:</span>
                    <span style="font-weight: 700; color: #F8FAFC;">{water_risk}</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 0.85rem;">
                    <span style="color: #94A3B8;">Monitoring Cadence:</span>
                    <span style="font-weight: 700; color: #F59E0B;">{cadence}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_repairs:
        st.subheader("🛠️ Recommended Engineering Repair Protocol")
        st.caption("Standardized rehabilitation per IS 14787 / ICRI 310.1R Specifications:")
        
        for rep in repairs:
            step_num = rep.get("step", 1)
            action = rep.get("action", "Repair Step")
            spec = rep.get("specification", "")

            st.markdown(
                f"""
                <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); 
                            border-radius: 8px; padding: 12px 16px; margin-bottom: 10px;">
                    <div style="display: flex; align-items: center; margin-bottom: 6px;">
                        <span style="background: #F59E0B; color: #0F172A; font-weight: 800; border-radius: 50%; 
                                     width: 24px; height: 24px; display: inline-flex; align-items: center; 
                                     justify-content: center; font-size: 0.8rem; margin-right: 10px;">
                            {step_num}
                        </span>
                        <span style="font-weight: 700; font-size: 0.95rem; color: #F8FAFC;">{action}</span>
                    </div>
                    <div style="color: #CBD5E1; font-size: 0.85rem; line-height: 1.4; padding-left: 34px;">
                        {spec}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Downloads
    st.markdown("---")
    d1, d2 = st.columns(2)
    with d1:
        st.download_button(
            label="📥 Download Forensic Diagnostic Telemetry (JSON)",
            data=json.dumps(data, indent=2),
            file_name=f"crack_diagnostics_{defect.replace(' ', '_').lower()}.json",
            mime="application/json",
            use_container_width=True
        )
    with d2:
        report_text = f"""# STRUCTURAL CRACK DIAGNOSTICS & INTEGRITY REPORT
Defect Classification: {defect}
Structural Element: {element}
Permissible Code: {code_ref}
Estimated Width: {width_mm:.2f} mm
Severity Index: {severity}
Remediation Urgency: {urgency}
Capacity Reduction: {risk.get('load_capacity_reduction_pct', 0)}%

ROOT CAUSES:
""" + "\n".join([f"- {c}" for c in causes]) + "\n\nREPAIR SPECIFICATION:\n" + "\n".join([f"Step {r.get('step')}: {r.get('action')} -> {r.get('specification')}" for r in repairs])

        st.download_button(
            label="📄 Download Engineering Repair Specification (Markdown)",
            data=report_text,
            file_name="structural_repair_spec.md",
            mime="text/markdown",
            use_container_width=True
        )
