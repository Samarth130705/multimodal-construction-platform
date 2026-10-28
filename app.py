"""
Multimodal Construction Intelligence Platform
Skill Wallet Capstone Project 1

Production-ready, 100% self-contained Streamlit application.
Integrates Google Gemini Multimodal Vision, OSHA 1926 & IS 456 compliance,
forensic structural crack diagnostics, CPWD valuation planning, and weather safety advisory.
Designed for 1-click zero-configuration deployment on Streamlit Community Cloud.
"""

import os
import sys
import io
import re
import json
import base64
import urllib.parse
from typing import Optional, Tuple, Dict, Any, List

# Ensure current directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import streamlit as st
from PIL import Image, ImageDraw

# =============================================================================
# STREAMLIT PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Modern Construction Dark UI Styling
CUSTOM_CSS = """
<style>
    .stApp {
        background: linear-gradient(135deg, #0B0F19 0%, #111827 50%, #0F172A 100%);
        color: #F8FAFC;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 16px 18px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(8px);
        margin-bottom: 12px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(245, 158, 11, 0.4);
    }
    .metric-label {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94A3B8;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        margin-top: 4px;
        line-height: 1.1;
    }
    .status-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.6);
        padding: 8px 10px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        border-radius: 8px;
        color: #94A3B8;
        font-weight: 600;
        font-size: 0.92rem;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%) !important;
        color: #0F172A !important;
        font-weight: 800;
    }
    .header-box {
        background: linear-gradient(90deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-left: 6px solid #F59E0B;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 24px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: #0F172A;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 8px 20px;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #FBBF24 0%, #F59E0B 100%);
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.35);
        color: #000;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =============================================================================
# GEMINI CLIENT & VISION INFERENCE ENGINE
# =============================================================================
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


def clean_json_text(raw_text: str) -> str:
    """Extracts JSON substring from markdown code blocks or outermost braces."""
    json_block = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
    if json_block:
        return json_block.group(1).strip()
    brace_match = re.search(r"(\{.*\})", raw_text, re.DOTALL)
    if brace_match:
        return brace_match.group(1).strip()
    return raw_text.strip()


def run_gemini_vision(
    prompt: str, 
    image_bytes: bytes, 
    mime_type: str = "image/jpeg", 
    api_key: Optional[str] = None,
    model_name: str = "gemini-2.5-flash"
) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    effective_key = api_key or os.environ.get("GEMINI_API_KEY", "").strip()
    
    if not effective_key:
        return False, None, "No Gemini API Key supplied. Demonstration Mode active."
    
    if not GENAI_AVAILABLE:
        return False, None, "google-genai SDK not installed in environment. Running in Demo Mode."

    try:
        client = genai.Client(api_key=effective_key)
        image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
        system_instruction = (
            "You are an expert civil and structural engineer and certified OSHA 1926 & IS 456 "
            "construction safety auditor. Always provide structured, engineering-accurate analysis. "
            "Always return your primary output in strict JSON format."
        )

        response = client.models.generate_content(
            model=model_name,
            contents=[image_part, prompt],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
                max_output_tokens=3000
            )
        )

        response_text = response.text or ""
        cleaned_json = clean_json_text(response_text)
        parsed = json.loads(cleaned_json)
        return True, parsed, "Live Gemini multimodal inference successful."

    except json.JSONDecodeError as jde:
        return True, None, f"Received response from Gemini, but JSON parsing failed: {str(jde)}"
    except Exception as e:
        return False, None, f"Gemini API request notice: {str(e)}. Fallback to demonstration telemetry."


def run_gemini_chat(
    history: list, 
    user_message: str, 
    system_context: str, 
    api_key: Optional[str] = None,
    model_name: str = "gemini-2.5-flash"
) -> str:
    effective_key = api_key or os.environ.get("GEMINI_API_KEY", "").strip()

    if not effective_key or not GENAI_AVAILABLE:
        return generate_demo_chat_reply(user_message)

    try:
        client = genai.Client(api_key=effective_key)
        formatted_contents = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            formatted_contents.append(
                types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
            )
        formatted_contents.append(
            types.Content(role="user", parts=[types.Part.from_text(text=user_message)])
        )

        response = client.models.generate_content(
            model=model_name,
            contents=formatted_contents,
            config=types.GenerateContentConfig(
                system_instruction=system_context,
                temperature=0.4,
                max_output_tokens=1500
            )
        )
        return response.text or "No response received."

    except Exception:
        return generate_demo_chat_reply(user_message)


def generate_demo_chat_reply(user_message: str) -> str:
    msg = user_message.lower()
    if "formwork" in msg or "stripping" in msg or "deshutter" in msg:
        return (
            "**Formwork Removal Minimum Periods (per IS 456:2000 Clause 11.3 & Table 1):**\n\n"
            "1. **Walls, columns, and vertical member faces**: 16 to 24 hours.\n"
            "2. **Slab soffits (props left under)**: 3 days (props refixed immediately).\n"
            "3. **Beam soffits (props left under)**: 7 days.\n"
            "4. **Removal of props under slabs**:\n"
            "   - Spanning up to 4.5 m: 7 days\n"
            "   - Spanning over 4.5 m: 14 days\n"
            "5. **Removal of props under beams and arches**:\n"
            "   - Spanning up to 6 m: 14 days\n"
            "   - Spanning over 6 m: 21 days\n\n"
            "*Safety Alert*: Extend these durations by 25-50% in cold weather (<15°C) or with mineral admixtures (PPC/GGBS)."
        )
    elif "crane" in msg or "wind" in msg or "lift" in msg:
        return (
            "**Tower Crane & Rigging Wind Safety Protocol (OSHA 1926.1431 & IS 875 Part 3):**\n\n"
            "- **Wind Speed < 32 km/h (9 m/s)**: Normal hoisting permitted with taglines.\n"
            "- **Wind Speed 32 - 38 km/h**: Cease hoisting large-surface panel loads (formwork panels, curtain wall glass).\n"
            "- **Wind Speed > 38 km/h (10.5 m/s) / Gale Warning**: Mandatory **STOP WORK** order. Disengage slewing brake to allow crane jib to weather-vane freely into the wind axis to prevent structural torsion failure."
        )
    elif "heat" in msg or "curing" in msg or "hot weather" in msg:
        return (
            "**Hot Weather Concreting Protocols (ACI 305R & IS 456:2000 Clause 13.5):**\n\n"
            "1. **Fresh Concrete Temperature**: Must not exceed 32°C at point of discharge. Utilize chilled batching water or flake ice substitution.\n"
            "2. **Plastic Shrinkage Crack Prevention**: If evaporation rate exceeds 1.0 kg/m²/hr, apply aliphatic alcohol evaporation retarders immediately after screeding.\n"
            "3. **Continuous Curing**: Enforce wet hessian burlap covering as soon as concrete sets. Keep continuously ponded for minimum 14 days."
        )
    else:
        return (
            f"**SiteSenior AI Engineering Advisory:**\n\n"
            f"Regarding your query on *\"{user_message}\"*:\n\n"
            "1. **Structural Verification**: Review site execution against approved GFC (Good-for-Construction) drawings and structural consultant specifications.\n"
            "2. **Code Benchmarking**: Verify adherence to IS 456:2000, batching calibration certificates, and 7/28-day concrete cube compressive tests (IS 516).\n"
            "3. **Safety Compliance**: Enforce 100% PPE compliance, double-hook lanyard tie-offs at elevations, and inspection tags on all temporary distribution boards."
        )

# =============================================================================
# SAMPLE ASSETS & SYNTHETIC TELEMETRY GENERATOR
# =============================================================================
def create_synthetic_image(title: str, subtitle: str, color_scheme: str = "safety") -> Image.Image:
    width, height = 800, 500
    if color_scheme == "safety":
        bg_color = (25, 33, 44)
        accent_color = (245, 158, 11)
        line_color = (71, 85, 105)
    elif color_scheme == "crack":
        bg_color = (38, 38, 38)
        accent_color = (239, 68, 68)
        line_color = (115, 115, 115)
    else:
        bg_color = (15, 23, 42)
        accent_color = (59, 130, 246)
        line_color = (51, 65, 85)

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    for x in range(0, width, 50):
        draw.line([(x, 0), (x, height)], fill=line_color, width=1)
    for y in range(0, height, 50):
        draw.line([(0, y), (width, y)], fill=line_color, width=1)

    draw.line([(0, 0), (width, height)], fill=line_color, width=2)
    draw.line([(0, height), (width, 0)], fill=line_color, width=2)

    if color_scheme == "crack":
        crack_points = [(150, 80), (220, 140), (290, 160), (360, 230), (420, 250), (490, 320), (550, 360), (620, 420)]
        draw.line(crack_points, fill=(15, 15, 15), width=7)
        draw.line(crack_points, fill=accent_color, width=2)
    elif color_scheme == "safety":
        draw.rectangle([(200, 150), (600, 380)], outline=accent_color, width=3)
        for i in range(200, 600, 40):
            draw.line([(i, 150), (i + 20, 170)], fill=accent_color, width=4)

    draw.rectangle([(40, 30), (width - 40, 110)], fill=(15, 23, 42, 220), outline=accent_color, width=2)
    draw.text((60, 45), f"SITE TELEMETRY CAPTURE // {title.upper()}", fill=(255, 255, 255))
    draw.text((60, 75), f"Standards: {subtitle} | Timecode: 10:42:18 IST", fill=accent_color)
    return img


def get_sample_image_bytes(category: str, sample_id: str = "sample_1") -> bytes:
    if category == "safety":
        if sample_id == "sample_1":
            img = create_synthetic_image("Zone 4B: Rebar Cage & Tower Crane Deck", "OSHA 1926.100 / IS 456 Safety Audit", "safety")
        else:
            img = create_synthetic_image("Zone 1A: Deep Shoring & Excavation Trench", "OSHA 1926.651 Trenching Protocol", "safety")
    elif category == "crack":
        if sample_id == "sample_1":
            img = create_synthetic_image("RC Girder Bay 7: 45° Diagonal Shear Fracture", "IS 456:2000 Cl. 40 Shear Assessment", "crack")
        else:
            img = create_synthetic_image("Cantilever Slab Soffit: Concrete Spalling & Rebar Rust", "IS 456 Cl. 26.4 Durability Diagnostic", "crack")
    else:
        img = create_synthetic_image("Civil Telemetry", "Inspection Record", "default")
    
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


def get_mock_safety_data(scenario: str = "sample_1") -> dict:
    if scenario == "sample_2":
        return {
            "safety_score": 58,
            "overall_status": "Critical Non-Compliance",
            "workers_detected_count": 3,
            "compliance_summary": "High-risk violations detected in trench zone. 1 operative within 2.5m excavation zone without hard hat or perimeter lifeline anchor.",
            "ppe_detection": [
                {"item": "Hard Hats / Safety Helmets", "status": "Non-Compliant", "detected_count": 1, "expected_count": 3, "compliance_rate": 33, "standard": "OSHA 1926.100 / IS 2925", "notes": "2 workers inside active excavation zone missing hard hats."},
                {"item": "High-Visibility Safety Vests", "status": "Partial", "detected_count": 2, "expected_count": 3, "compliance_rate": 67, "standard": "OSHA 1926.201 / EN ISO 20471", "notes": "1 worker wearing non-reflective dark clothing adjacent to excavator swing path."},
                {"item": "Steel-Toe Safety Footwear", "status": "Compliant", "detected_count": 3, "expected_count": 3, "compliance_rate": 100, "standard": "OSHA 1926.96 / IS 15298", "notes": "Steel-toe puncture resistant boots verified on all operatives."},
                {"item": "Trench Fall Arrest / Harness", "status": "Non-Compliant", "detected_count": 0, "expected_count": 3, "compliance_rate": 0, "standard": "OSHA 1926.502 / IS 3521", "notes": "No harness or retrieve lifeline tethering near trench collapse zone."}
            ],
            "site_hazards": [
                {"hazard": "Trench Shoring & Unprotected Edge", "severity": "Critical", "location_zone": "Trench Bay 2", "regulatory_violation": "OSHA 1926.652 & IS 3764:1992", "corrective_remedy": "Immediately halt work. Install hydraulic trench box shoring before re-entry."},
                {"hazard": "Excavator Swing Radius Struck-By Risk", "severity": "High", "location_zone": "Zone 1A Corridor", "regulatory_violation": "OSHA 1926.600", "corrective_remedy": "Demarcate 5m red exclusion zone with warning barriers and dedicated banksman."}
            ]
        }
    return {
        "safety_score": 84,
        "overall_status": "Warning - Action Required",
        "workers_detected_count": 4,
        "compliance_summary": "Good overall baseline compliance on rebar framing deck. 4/4 hard hats and safety boots verified. Fall arrest lanyard anchor violation noted at level 3 scaffolding perimeter.",
        "ppe_detection": [
            {"item": "Hard Hats / Safety Helmets", "status": "Compliant", "detected_count": 4, "expected_count": 4, "compliance_rate": 100, "standard": "OSHA 1926.100 / IS 2925", "notes": "All 4 operatives wearing chinstrap-secured industrial safety helmets."},
            {"item": "High-Visibility Safety Vests", "status": "Compliant", "detected_count": 4, "expected_count": 4, "compliance_rate": 100, "standard": "OSHA 1926.201 / EN ISO 20471", "notes": "Fluorescent yellow/orange retroreflective vests clearly visible."},
            {"item": "Steel-Toe Safety Footwear", "status": "Compliant", "detected_count": 4, "expected_count": 4, "compliance_rate": 100, "standard": "OSHA 1926.96 / IS 15298", "notes": "Verified steel toe puncture-proof site boots on all personnel."},
            {"item": "Fall Arrest Harness & Lifeline Anchor", "status": "Partial", "detected_count": 2, "expected_count": 4, "compliance_rate": 50, "standard": "OSHA 1926.502 / IS 3521", "notes": "2 workers at slab edge have harnesses worn, but secondary safety lanyard is unhooked."}
        ],
        "site_hazards": [
            {"hazard": "Unanchored Fall Arrest Lanyard at Perimeter", "severity": "High", "location_zone": "Level 3 Slab Edge Cantilever", "regulatory_violation": "OSHA 1926.501(b)(1) & IS 3521", "corrective_remedy": "Enforce 100% tie-off protocol immediately. Clip double-scaffold hooks to certified 8mm wire rope static line."},
            {"hazard": "Unprotected Impalement Hazard from Rebar Dowels", "severity": "Medium", "location_zone": "Bay 4 Column Starter Bars", "regulatory_violation": "OSHA 1926.701(b) & IS 456", "corrective_remedy": "Cap all exposed vertical steel rebar ends with OSHA-approved mushroom steel-reinforced caps."}
        ]
    }


def get_mock_crack_data(scenario: str = "sample_1") -> dict:
    if scenario == "sample_2":
        return {
            "defect_type": "Concrete Spalling & Rebar Delamination",
            "estimated_crack_width_mm": 4.2,
            "severity_index": "Critical Structural Defect",
            "urgency": "Immediate Structural Evacuation / Shoring",
            "structural_element": "Cantilever Balcony Slab Soffit",
            "is_code_reference": "IS 456:2000 Clause 26.4 (Durability) & Clause 35.3",
            "root_causes": [
                "Carbonation and aggressive chloride ingress through inadequate 15mm concrete cover.",
                "Oxidation of tensile reinforcement leading to rust expansion up to 600% volume.",
                "Delamination and complete shear spalling of concrete cover layer."
            ],
            "engineering_repairs": [
                {"step": 1, "action": "Immediate Temporary Shoring", "specification": "Install adjustable steel prop towers (Acro props) at 1.0m c/c beneath cantilever span."},
                {"step": 2, "action": "Chipping & Substrate Preparation", "specification": "Chisel back sound concrete 20mm behind corroded rebar per ICRI Technical Guideline 310.1R."},
                {"step": 3, "action": "Rebar De-Rusting & Passivation", "specification": "Mechanical grit blast rebar to SA 2.5 finish. Apply 2 coats of zinc-rich epoxy anti-corrosion primer."},
                {"step": 4, "action": "Polymer Modified Mortar Patching", "specification": "Apply SBR bonding coat followed by structural low-shrinkage fiber-reinforced repair mortar."}
            ],
            "risk_assessment": {"load_capacity_reduction_pct": 35, "water_ingress_risk": "Severe", "monitoring_frequency": "Continuous until shoring installed"}
        }
    return {
        "defect_type": "Structural Shear Crack",
        "estimated_crack_width_mm": 1.85,
        "severity_index": "High Engineering Risk",
        "urgency": "High Priority (Remediate within 7 days)",
        "structural_element": "Reinforced Concrete Transfer Girder",
        "is_code_reference": "IS 456:2000 Clause 40 (Design for Shear) & Clause 43.1",
        "root_causes": [
            "Excessive principal tensile stress inclined at approximately 45 degrees near beam support.",
            "Inadequate shear reinforcement (stirrup spacing > 0.75d) for redistributed construction crane loads.",
            "Dynamic load amplification from heavy material staging directly above girder span."
        ],
        "engineering_repairs": [
            {"step": 1, "action": "Load Relieving & De-Staging", "specification": "Immediately clear all stacked bricks, rebar bundles, and wet mortar tubs from the top flange of the transfer girder."},
            {"step": 2, "action": "Surface Preparation & Port Installation", "specification": "V-groove crack to 15x15mm along full fracture path. Bond injection nipple packers at 200mm intervals using rapid epoxy putty."},
            {"step": 3, "action": "Low-Viscosity Epoxy Pressure Grouting", "specification": "Inject high-modulus, low-viscosity structural epoxy resin (ASTM C881 Type I/IV Grade 1) under 0.2 to 0.4 MPa pressure."},
            {"step": 4, "action": "External Shear Banding / CFRP U-Wraps", "specification": "Install dual-layer 450 gsm unidirectional Carbon Fiber U-jackets anchored into beam top flange."}
        ],
        "risk_assessment": {"load_capacity_reduction_pct": 22, "water_ingress_risk": "Moderate", "monitoring_frequency": "Every 48 hours until epoxy curing inspection test"}
    }

# =============================================================================
# TAB 1: SAFETY AUDIT MODULE
# =============================================================================
SAFETY_AUDIT_PROMPT = """
You are an accredited Senior Construction Safety Auditor and OSHA / Bureau of Indian Standards (IS 456 / IS 2925) Compliance Inspector.
Inspect this construction site image with high precision. Analyze worker PPE compliance and identify environmental and structural hazards.

Output MUST be a strict, valid JSON object with the exact following schema:
{
  "safety_score": <integer from 0 to 100>,
  "overall_status": "<'Compliant' | 'Warning - Action Required' | 'Critical Non-Compliance'>",
  "compliance_summary": "<concise 2-sentence summary>",
  "workers_detected_count": <integer count>,
  "ppe_detection": [
    {
      "item": "Hard Hats / Safety Helmets",
      "status": "<'Compliant' | 'Partial' | 'Non-Compliant'>",
      "detected_count": <int>,
      "expected_count": <int>,
      "compliance_rate": <int 0-100>,
      "standard": "OSHA 1926.100 / IS 2925",
      "notes": "<observation>"
    },
    {
      "item": "High-Visibility Safety Vests",
      "status": "<'Compliant' | 'Partial' | 'Non-Compliant'>",
      "detected_count": <int>,
      "expected_count": <int>,
      "compliance_rate": <int 0-100>,
      "standard": "OSHA 1926.201 / EN ISO 20471",
      "notes": "<observation>"
    },
    {
      "item": "Steel-Toe Protective Footwear",
      "status": "<'Compliant' | 'Partial' | 'Non-Compliant'>",
      "detected_count": <int>,
      "expected_count": <int>,
      "compliance_rate": <int 0-100>,
      "standard": "OSHA 1926.96 / IS 15298",
      "notes": "<observation>"
    },
    {
      "item": "Fall Arrest Harness & Lifelines",
      "status": "<'Compliant' | 'Partial' | 'Non-Compliant'>",
      "detected_count": <int>,
      "expected_count": <int>,
      "compliance_rate": <int 0-100>,
      "standard": "OSHA 1926.502 / IS 3521",
      "notes": "<observation>"
    }
  ],
  "site_hazards": [
    {
      "hazard": "<hazard title>",
      "severity": "<'Low' | 'Medium' | 'High' | 'Critical'>",
      "location_zone": "<location>",
      "regulatory_violation": "<OSHA / IS standard clause>",
      "corrective_remedy": "<remedial engineering action>"
    }
  ]
}
Return only JSON.
"""

def execute_safety_audit(image_bytes: bytes, mime_type: str = "image/jpeg", api_key: Optional[str] = None, sample_id: str = "sample_1") -> Tuple[Dict[str, Any], bool, str]:
    if api_key and len(api_key.strip()) > 10:
        is_live, parsed, msg = run_gemini_vision(SAFETY_AUDIT_PROMPT, image_bytes, mime_type, api_key)
        if is_live and parsed and "safety_score" in parsed:
            return parsed, True, msg
    return get_mock_safety_data(sample_id), False, "Demonstration Mode Active (High-Fidelity Telemetry Simulation)"


def render_safety_audit_view(data: Dict[str, Any], is_live: bool, status_msg: str):
    score = data.get("safety_score", 0)
    overall_status = data.get("overall_status", "Unknown")
    workers_count = data.get("workers_detected_count", 0)
    hazards = data.get("site_hazards", [])
    ppe_items = data.get("ppe_detection", [])
    summary = data.get("compliance_summary", "")

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
            <div style="font-size: 0.85rem; color: #94A3B8;">{status_msg}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    m1, m2, m3, m4 = st.columns(4)
    score_color = "#10B981" if score >= 80 else ("#F59E0B" if score >= 60 else "#EF4444")
    status_bg = "rgba(16, 185, 129, 0.2)" if score >= 80 else ("rgba(245, 158, 11, 0.2)" if score >= 60 else "rgba(239, 68, 68, 0.2)")

    with m1:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 4px solid {score_color};">
                <div class="metric-label">Safety Compliance Score</div>
                <div class="metric-value" style="color: {score_color};">{score}<span style="font-size:1.2rem; color:#94A3B8;">/100</span></div>
            </div>
            """, unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 4px solid {score_color};">
                <div class="metric-label">Overall Site Status</div>
                <div style="margin-top: 10px;">
                    <span class="status-pill" style="background: {status_bg}; color: {score_color}; border: 1px solid {score_color};">{overall_status}</span>
                </div>
            </div>
            """, unsafe_allow_html=True
        )
    with m3:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 4px solid #3B82F6;">
                <div class="metric-label">Operatives in Frame</div>
                <div class="metric-value" style="color: #60A5FA;">{workers_count} <span style="font-size:1rem; color:#94A3B8;">Workers</span></div>
            </div>
            """, unsafe_allow_html=True
        )
    with m4:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 4px solid #EF4444;">
                <div class="metric-label">Identified Hazards</div>
                <div class="metric-value" style="color: #EF4444;">{len(hazards)} <span style="font-size:0.9rem; color:#94A3B8;">Detected</span></div>
            </div>
            """, unsafe_allow_html=True
        )

    if summary:
        st.info(f"📋 **Site Safety Executive Brief:** {summary}")

    st.markdown("---")
    col_left, col_right = st.columns([1.1, 0.9])

    with col_left:
        st.subheader("🛡️ PPE Compliance Detection Checklist (OSHA & IS 456)")
        for item in ppe_items:
            status = item.get("status", "Unknown")
            badge_color = "#10B981" if status.lower() == "compliant" else ("#F59E0B" if status.lower() == "partial" else "#EF4444")
            icon = "✅" if status.lower() == "compliant" else ("⚠️" if status.lower() == "partial" else "❌")

            st.markdown(
                f"""
                <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); 
                            border-radius: 8px; padding: 12px 16px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-weight: 600; font-size: 1rem; color: #F1F5F9;">{item.get('item')}</span>
                        <span style="color: {badge_color}; border: 1px solid {badge_color}; padding: 2px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700;">
                            {icon} {status.upper()} ({item.get('compliance_rate', 0)}%)
                        </span>
                    </div>
                    <div style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 4px;">Standard: <code>{item.get('standard')}</code> | Detected: {item.get('detected_count', 0)} / {item.get('expected_count', workers_count)}</div>
                    <div style="font-size: 0.85rem; color: #CBD5E1;">{item.get('notes')}</div>
                </div>
                """, unsafe_allow_html=True
            )

    with col_right:
        st.subheader("⚠️ Site Hazards & Corrective Remedies")
        for idx, hz in enumerate(hazards, 1):
            sev = hz.get("severity", "Medium")
            s_color = "#EF4444" if sev.lower() == "critical" else ("#F97316" if sev.lower() == "high" else "#F59E0B")
            with st.expander(f"[{sev.upper()}] {hz.get('hazard')}", expanded=(idx <= 2)):
                st.markdown(f"**📍 Location:** {hz.get('location_zone')}")
                st.markdown(f"**⚖️ Standard Violated:** `{hz.get('regulatory_violation')}`")
                st.markdown(
                    f"""
                    <div style="background: rgba(239, 68, 68, 0.08); border-left: 3px solid {s_color}; padding: 8px 12px; border-radius: 4px; margin-top: 8px;">
                        <b>Corrective Remedy:</b><br/><span style="color: #E2E8F0; font-size: 0.9rem;">{hz.get('corrective_remedy')}</span>
                    </div>
                    """, unsafe_allow_html=True
                )

    st.markdown("---")
    d1, d2 = st.columns(2)
    with d1:
        st.download_button("📥 Download Audit Report (JSON)", data=json.dumps(data, indent=2), file_name="site_safety_audit.json", mime="application/json", use_container_width=True)
    with d2:
        st.download_button("📄 Download Markdown Brief", data=f"# Safety Audit\nScore: {score}/100\nStatus: {overall_status}\nSummary: {summary}", file_name="site_safety_brief.md", mime="text/markdown", use_container_width=True)

# =============================================================================
# TAB 2: CRACK DIAGNOSTICS MODULE
# =============================================================================
CRACK_DIAGNOSTICS_PROMPT = """
You are a Principal Forensic Structural Engineer (IS 456:2000, ACI 224.1R certified).
Analyze the structural concrete/wall defect photo. Classify defect type (Hairline, Settlement, Structural Shear, Thermal, Spalling).
Output MUST be strict JSON:
{
  "defect_type": "<'Hairline Crack' | 'Settlement Crack' | 'Structural Shear Crack' | 'Thermal Expansion Crack' | 'Concrete Spalling & Rebar Delamination'>",
  "estimated_crack_width_mm": <float width in mm>,
  "severity_index": "<severity>",
  "urgency": "<urgency>",
  "structural_element": "<element>",
  "is_code_reference": "<IS 456 clause>",
  "root_causes": ["<cause 1>", "<cause 2>"],
  "engineering_repairs": [{"step": 1, "action": "<procedure>", "specification": "<spec>"}],
  "risk_assessment": {"load_capacity_reduction_pct": <int 0-100>, "water_ingress_risk": "<risk>", "monitoring_frequency": "<cadence>"}
}
"""

def execute_crack_diagnostics(image_bytes: bytes, mime_type: str = "image/jpeg", api_key: Optional[str] = None, sample_id: str = "sample_1") -> Tuple[Dict[str, Any], bool, str]:
    if api_key and len(api_key.strip()) > 10:
        is_live, parsed, msg = run_gemini_vision(CRACK_DIAGNOSTICS_PROMPT, image_bytes, mime_type, api_key)
        if is_live and parsed and "defect_type" in parsed:
            return parsed, True, msg
    return get_mock_crack_data(sample_id), False, "Demonstration Mode Active (Forensic Structural Telemetry)"


def render_crack_diagnostics_view(data: Dict[str, Any], is_live: bool, status_msg: str):
    defect = data.get("defect_type", "Structural Crack")
    width_mm = data.get("estimated_crack_width_mm", 0.0)
    urgency = data.get("urgency", "Monitor")
    element = data.get("structural_element", "RC Member")
    code_ref = data.get("is_code_reference", "IS 456:2000")
    causes = data.get("root_causes", [])
    repairs = data.get("engineering_repairs", [])
    risk = data.get("risk_assessment", {})

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
            <div style="font-size: 0.85rem; color: #94A3B8;">{status_msg}</div>
        </div>
        """, unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)
    w_color = "#EF4444" if width_mm > 1.5 else ("#F59E0B" if width_mm > 0.3 else "#10B981")
    u_color = "#EF4444" if "immediate" in urgency.lower() else ("#F97316" if "high" in urgency.lower() else "#10B981")

    with c1:
        st.markdown(f'<div class="metric-card" style="border-left: 4px solid #3B82F6;"><div class="metric-label">Defect Classification</div><div style="font-size: 1.25rem; font-weight: 700; color: #60A5FA; margin-top: 6px;">{defect}</div><div style="font-size:0.75rem; color:#94A3B8;">Element: {element}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card" style="border-left: 4px solid {w_color};"><div class="metric-label">Estimated Width</div><div class="metric-value" style="color: {w_color};">{width_mm:.2f} <span style="font-size:1.1rem; color:#94A3B8;">mm</span></div><div style="font-size:0.72rem; color:#CBD5E1;">{"⚠️ Exceeds IS 456 Limit (0.3mm)" if width_mm > 0.3 else "✅ Within Limit"}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card" style="border-left: 4px solid {u_color};"><div class="metric-label">Remediation Urgency</div><div style="margin-top: 8px;"><span class="status-pill" style="background: rgba(239, 68, 68, 0.2); color: {u_color}; border: 1px solid {u_color};">{urgency}</span></div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card" style="border-left: 4px solid #8B5CF6;"><div class="metric-label">Capacity Impairment</div><div class="metric-value" style="color: #A78BFA;">-{risk.get("load_capacity_reduction_pct", 0)}% <span style="font-size:0.9rem; color:#94A3B8;">Loss</span></div><div style="font-size:0.75rem; color:#94A3B8;">Code: <code>{code_ref}</code></div></div>', unsafe_allow_html=True)

    st.markdown("---")
    col_causes, col_repairs = st.columns([1, 1.3])

    with col_causes:
        st.subheader("🔬 Forensic Root Causes")
        for idx, cause in enumerate(causes, 1):
            st.markdown(f'<div style="background: rgba(30, 41, 59, 0.6); border-left: 3px solid #3B82F6; padding: 10px 14px; border-radius: 6px; margin-bottom: 10px; font-size: 0.9rem; color: #E2E8F0;"><b>{idx}.</b> {cause}</div>', unsafe_allow_html=True)

    with col_repairs:
        st.subheader("🛠️ Recommended Repair Protocol")
        for rep in repairs:
            st.markdown(
                f"""
                <div style="background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 12px 16px; margin-bottom: 10px;">
                    <div style="font-weight: 700; color: #F59E0B; margin-bottom: 4px;">Step {rep.get('step')}: {rep.get('action')}</div>
                    <div style="color: #CBD5E1; font-size: 0.85rem; line-height: 1.4;">{rep.get('specification')}</div>
                </div>
                """, unsafe_allow_html=True
            )

    st.markdown("---")
    cd1, cd2 = st.columns(2)
    with cd1:
        st.download_button("📥 Download Diagnostic Telemetry (JSON)", data=json.dumps(data, indent=2), file_name="crack_diagnostics.json", mime="application/json", use_container_width=True)
    with cd2:
        st.download_button("📄 Download Repair Specification", data=f"# Structural Diagnostics\nDefect: {defect}\nWidth: {width_mm}mm\nUrgency: {urgency}", file_name="structural_repairs.md", mime="text/markdown", use_container_width=True)

# =============================================================================
# TAB 3: PLANNING & VALUATION MODULE
# =============================================================================
STRUCTURE_SPECS = {
    "Residential High-Rise (RCC Mivan / Shear Wall)": {"tier1_rate": 2600, "tier2_rate": 2100, "tier3_rate": 1750, "steel_kg_sqft": 4.6, "cement_bags_sqft": 0.43, "market_multiple": 3.6, "render_desc": "luxurious contemporary high-rise residential apartment tower with glass balconies, landscaped podium, infinity pool, modern Indian skyline"},
    "Commercial Grade-A Office Complex": {"tier1_rate": 3600, "tier2_rate": 2900, "tier3_rate": 2300, "steel_kg_sqft": 5.4, "cement_bags_sqft": 0.49, "market_multiple": 4.2, "render_desc": "state-of-the-art grade-A corporate tech park, parametric glass curtain facade, double-height grand lobby, biophilic atrium"},
    "Industrial PEB Warehouse & Logistics Hub": {"tier1_rate": 1900, "tier2_rate": 1550, "tier3_rate": 1250, "steel_kg_sqft": 6.8, "cement_bags_sqft": 0.28, "market_multiple": 2.2, "render_desc": "large modern pre-engineered industrial logistics warehouse, automated docking bays, solar roof panels, clean concrete apron"},
    "Luxury Villa / Premium Bungalow Estate": {"tier1_rate": 4500, "tier2_rate": 3600, "tier3_rate": 2900, "steel_kg_sqft": 4.9, "cement_bags_sqft": 0.46, "market_multiple": 3.8, "render_desc": "minimalist tropical modern luxury villa, cantilevered wooden louvers, expansive travertine terrace, reflection pool"},
    "Mixed-Use Commercial & Retail Mall": {"tier1_rate": 3300, "tier2_rate": 2650, "tier3_rate": 2150, "steel_kg_sqft": 5.1, "cement_bags_sqft": 0.45, "market_multiple": 3.9, "render_desc": "dynamic mixed-use retail lifestyle center and urban plaza, illuminated storefronts, pedestrian promenade"}
}

FINISH_MULTIPLIERS = {"Standard / Economy": 1.00, "Premium / Semi-Luxury": 1.25, "Ultra-Luxury / Bespoke High-End": 1.60}

def format_inr(amount: float) -> Tuple[str, str]:
    if amount >= 10000000:
        cr = amount / 10000000
        return f"₹{cr:.2f} Cr", f"{cr:.2f} Crores"
    elif amount >= 100000:
        lk = amount / 100000
        return f"₹{lk:.2f} L", f"{lk:.2f} Lakhs"
    return f"₹{amount:,.0f}", f"₹{amount:,.0f}"


def calculate_project_metrics(structure_type: str, built_up_sqft: float, tier: str, finish_grade: str, completion_pct: float) -> Dict[str, Any]:
    spec = STRUCTURE_SPECS[structure_type]
    finish_mult = FINISH_MULTIPLIERS[finish_grade]
    base_rate = spec["tier1_rate"] if "Tier 1" in tier else (spec["tier2_rate"] if "Tier 2" in tier else spec["tier3_rate"])

    effective_rate = base_rate * finish_mult
    total_budget = built_up_sqft * effective_rate
    capex_incurred = total_budget * (completion_pct / 100.0)
    completed_value = total_budget * spec["market_multiple"]
    land_equity = total_budget * 0.40
    accrued_surplus = (completed_value - total_budget - land_equity) * (completion_pct / 100.0)
    current_valuation = land_equity + capex_incurred + max(0, accrued_surplus)

    steel_mt = (built_up_sqft * spec["steel_kg_sqft"]) / 1000.0
    cement_bags = built_up_sqft * spec["cement_bags_sqft"]

    return {
        "total_budget": total_budget,
        "effective_rate": effective_rate,
        "capex_incurred": capex_incurred,
        "current_valuation": current_valuation,
        "completed_value": completed_value,
        "steel_mt": steel_mt,
        "cement_bags": cement_bags,
        "render_desc": spec["render_desc"]
    }


def generate_pollinations_url(structure_type: str, tier: str, custom_keywords: str = "", lighting: str = "Dramatic Sunset Golden Hour", seed: int = 108) -> str:
    desc = STRUCTURE_SPECS[structure_type]["render_desc"]
    prompt = f"Hyperrealistic 8k architectural exterior of a {desc}, located in {tier} Indian metro, {lighting}, photorealistic reflections, cinematic composition"
    if custom_keywords:
        prompt += f", {custom_keywords}"
    encoded = urllib.parse.quote_plus(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=640&seed={seed}&nologo=true"


def render_valuation_planner_view():
    st.subheader("🏗️ Project Financial Planning, CapEx & Valuation")
    st.caption("Standardized CPWD DSR benchmarks, Indian city tier indices, and generative 3D visualization.")

    c1, c2 = st.columns([1.2, 1])
    with c1:
        st_type = st.selectbox("🏢 Structure Typology", options=list(STRUCTURE_SPECS.keys()), index=0)
    with c2:
        loc_tier = st.selectbox("📍 Location Tier", options=["Tier 1 - Mumbai, Delhi-NCR, Bengaluru (1.0x)", "Tier 2 - Pune, Ahmedabad, Chandigarh (0.82x)", "Tier 3 - Emerging Hubs (0.68x)"], index=0)

    rc1, rc2, rc3 = st.columns(3)
    with rc1:
        sqft = st.number_input("📐 Built-Up Area (Sq.Ft.)", min_value=1000, max_value=2000000, value=75000, step=5000)
    with rc2:
        fin = st.selectbox("✨ Finishes", options=list(FINISH_MULTIPLIERS.keys()), index=1)
    with rc3:
        comp = st.slider("📊 Completion Progress (%)", min_value=0, max_value=100, value=45, step=5)

    m = calculate_project_metrics(st_type, sqft, loc_tier, fin, comp)
    b_fmt, _ = format_inr(m["total_budget"])
    c_fmt, _ = format_inr(m["capex_incurred"])
    v_fmt, _ = format_inr(m["current_valuation"])
    d_fmt, _ = format_inr(m["completed_value"])

    st.markdown("---")
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown(f'<div class="metric-card" style="border-left: 4px solid #3B82F6;"><div class="metric-label">Estimated Budget</div><div class="metric-value" style="color: #60A5FA;">{b_fmt}</div><div style="font-size: 0.75rem; color:#94A3B8;">Rate: ₹{m["effective_rate"]:,.0f} / sqft</div></div>', unsafe_allow_html=True)
    with f2:
        st.markdown(f'<div class="metric-card" style="border-left: 4px solid #F59E0B;"><div class="metric-label">CapEx Incurred</div><div class="metric-value" style="color: #FBBF24;">{c_fmt}</div><div style="font-size: 0.75rem; color:#94A3B8;">{comp}% budget spent</div></div>', unsafe_allow_html=True)
    with f3:
        st.markdown(f'<div class="metric-card" style="border-left: 4px solid #10B981;"><div class="metric-label">Current Asset Valuation</div><div class="metric-value" style="color: #34D399;">{v_fmt}</div><div style="font-size: 0.75rem; color:#94A3B8;">Includes land equity</div></div>', unsafe_allow_html=True)
    with f4:
        st.markdown(f'<div class="metric-card" style="border-left: 4px solid #A855F7;"><div class="metric-label">Target Completion Value</div><div class="metric-value" style="color: #C084FC;">{d_fmt}</div><div style="font-size: 0.75rem; color:#94A3B8;">Projected delivery gross</div></div>', unsafe_allow_html=True)

    st.markdown("#### 🚩 Milestone Progress")
    st.progress(comp / 100.0)

    st.markdown("---")
    st.subheader("📦 Core Material Quantities (CPWD Norms)")
    mc1, mc2 = st.columns(2)
    with mc1:
        st.info(f"**Structural Rebar (Fe550 TMT):** `{m['steel_mt']:,.1f} Metric Tonnes` (~{m['steel_mt'] * (comp/100):,.1f} MT consumed)")
    with mc2:
        st.info(f"**Cement (OPC / PPC 50kg Bags):** `{m['cement_bags']:,.0f} Bags` (~{m['cement_bags'] * 0.05:,.1f} MT)")

    st.markdown("---")
    st.subheader("🎨 Conceptual 3D Architectural Rendering (Pollinations AI)")
    light = st.selectbox("🌅 Lighting Atmosphere", ["Dramatic Sunset Golden Hour", "Crisp Daylight", "Twilight Blue Hour"], index=0)
    url = generate_pollinations_url(st_type, loc_tier, lighting=light)
    st.image(url, caption="Conceptual 3D Perspective (Pollinations Generative Architecture Engine)", use_container_width=True)

# =============================================================================
# TAB 4: WEATHER ADVISORY & SITE ASSISTANT MODULE
# =============================================================================
WEATHER_PROTOCOLS = {
    "High Wind (>40 km/h / Gale Warning)": {"level": "CRITICAL OPERATIONAL ALERT", "color": "#EF4444", "rule": "Halt tower crane & hoist operations (OSHA 1926.1431). Release slewing brake for free weather-vaning. Evacuate external suspended scaffolding."},
    "Heavy Rain / Monsoon Storm": {"level": "HIGH WEATHER ALERT", "color": "#3B82F6", "rule": "Activate basement de-watering pumps. Inspect trench slope berms (IS 3764). De-energize temporary 415V electrical distribution boxes."},
    "Extreme Heat (>42°C / Heatwave Alert)": {"level": "SEVERE CLIMATIC ADVISORY", "color": "#F97316", "rule": "IS 456 Cl. 13.5 hot-weather concreting. Concrete discharge temp <32°C with chilled water. Continuous 14-day wet hessian ponding. Mandatory worker hydration shifts."},
    "Cold Wave / Dense Fog (<8°C / Low Visibility)": {"level": "MODERATE OPERATIONAL ADVISORY", "color": "#A855F7", "rule": "Extend formwork removal stripping times by 35% (IS 456 Cl. 11.3). Deploy perimeter high-mast safety lighting."},
    "Normal / Clear Weather": {"level": "STANDARD OPERATING CONDITIONS", "color": "#10B981", "rule": "Full-speed superstructure and facade operations approved under standard OSHA 1926 PPE compliance."}
}

def render_weather_assistant_view(api_key: Optional[str] = None):
    st.subheader("🌤️ Weather-Aware Daily Site Advisory & Safety Protocols")
    cond = st.selectbox("⚡ Current Environmental Condition at Site", options=list(WEATHER_PROTOCOLS.keys()), index=0)
    w_info = WEATHER_PROTOCOLS[cond]

    st.markdown(
        f"""
        <div style="background: rgba(30, 41, 59, 0.8); border: 2px solid {w_info['color']}; border-radius: 10px; padding: 16px 20px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <b style="color: {w_info['color']}; font-size: 0.95rem;">{w_info['level']}</b>
            </div>
            <div style="color: #F8FAFC; font-size: 1.05rem; font-weight: 700;">{w_info['rule']}</div>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("---")
    st.subheader("💬 SiteSenior AI: Lead Resident Civil Engineer Chatbot")
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [{"role": "model", "content": "**Greetings Engineer.** I am **SiteSenior AI**, your lead resident civil engineer. Ask about IS 456, formwork stripping times, crane wind rules, or concrete mix adjustments."}]

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"], avatar="👷‍♂️" if msg["role"] == "user" else "🤖"):
            st.markdown(msg["content"])

    user_query = st.chat_input("Ask a civil engineering or site safety question...")
    if user_query:
        st.session_state.chat_messages.append({"role": "user", "content": user_query})
        with st.chat_message("user", avatar="👷‍♂️"):
            st.markdown(user_query)

        with st.chat_message("model", avatar="🤖"):
            with st.spinner("SiteSenior AI is computing structural standards..."):
                reply = run_gemini_chat(st.session_state.chat_messages[:-1], user_query, f"Active Weather: {cond}", api_key=api_key)
                st.markdown(reply)
        st.session_state.chat_messages.append({"role": "model", "content": reply})


# =============================================================================
# MAIN ORCHESTRATION & SIDEBAR
# =============================================================================
def main():
    if "api_key" not in st.session_state:
        st.session_state.api_key = os.environ.get("GEMINI_API_KEY", "")
    if "safety_results" not in st.session_state:
        st.session_state.safety_results = None
    if "crack_results" not in st.session_state:
        st.session_state.crack_results = None

    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 16px;">
                <span style="font-size: 2.4rem;">🏗️</span>
                <div style="font-size: 1.15rem; font-weight: 800; color: #F59E0B;">CONSTRUCTION INTELLIGENCE</div>
                <div style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase;">Skill Wallet Capstone Project 1</div>
            </div>
            """, unsafe_allow_html=True
        )
        st.subheader("🔑 Gemini API Configuration")
        user_key = st.text_input("Google Gemini API Key", type="password", value=st.session_state.api_key, placeholder="AIzaSy... (Leave empty for Demo Mode)")
        if user_key != st.session_state.api_key:
            st.session_state.api_key = user_key

        if st.session_state.api_key and len(st.session_state.api_key.strip()) > 10:
            st.markdown('<div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; border-radius: 6px; padding: 6px 12px; text-align: center;"><span style="color: #34D399; font-size: 0.82rem; font-weight: 700;">🟢 LIVE API ACTIVE (Gemini 2.5 Flash)</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="background: rgba(245, 158, 11, 0.15); border: 1px solid #F59E0B; border-radius: 6px; padding: 6px 12px; text-align: center;"><span style="color: #FBBF24; font-size: 0.82rem; font-weight: 700;">🟡 DEMONSTRATION MODE ACTIVE</span></div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🏛️ Standards\n- **OSHA 29 CFR 1926**\n- **IS 456:2000 (Concrete)**\n- **IS 875 (Wind Loads)**\n- **CPWD DSR Benchmarks**")

    # Header Box
    st.markdown(
        """
        <div class="header-box">
            <h1 style="margin: 0; font-size: 2.1rem; font-weight: 800; color: #F8FAFC;">Multimodal Construction Intelligence Platform</h1>
            <div style="color: #F59E0B; font-size: 0.95rem; font-weight: 600; margin-top: 4px;">
                Site Safety Auditing • Forensic Crack Diagnostics • Real Estate Valuation • Daily Field Advisory
            </div>
        </div>
        """, unsafe_allow_html=True
    )

    t1, t2, t3, t4 = st.tabs([
        "🛡️ Site Safety & PPE Audit (Epic 2)",
        "🔍 Crack Diagnostics & Integrity (Epic 2)",
        "📐 Planning & Real Estate Valuation (Epic 3)",
        "🌤️ Daily Site Assistant & Weather Advisory (Epic 5)"
    ])

    with t1:
        st.subheader("🛡️ Construction Site Safety & PPE Compliance Audit")
        u1, u2 = st.columns([1.2, 0.8])
        with u1:
            up_file = st.file_uploader("Upload Construction Site Photo (JPG / PNG)", type=["jpg", "jpeg", "png"], key="safety_up")
        with u2:
            s_choice = st.selectbox("Or Test with Pre-Loaded Telemetry", ["Sample 1: Active Rebar Deck", "Sample 2: Deep Trench Hazard"], key="safety_choice")
            s_id = "sample_1" if "Sample 1" in s_choice else "sample_2"
            load_s = st.button("📥 Load Sample Capture", use_container_width=True, key="load_safety_btn")

        img_b = None
        if up_file:
            img_b = up_file.getvalue()
        elif load_s or "act_safety_b" in st.session_state:
            if load_s:
                st.session_state.act_safety_b = get_sample_image_bytes("safety", s_id)
                st.session_state.act_safety_id = s_id
                st.session_state.safety_results = None
            img_b = st.session_state.get("act_safety_b")
            s_id = st.session_state.get("act_safety_id", "sample_1")

        if img_b:
            ic1, ic2 = st.columns([1, 1.2])
            with ic1:
                st.image(img_b, caption="Active Site Telemetry", use_container_width=True)
            with ic2:
                if st.button("🚀 Execute Multimodal Safety Audit", key="run_s_audit", use_container_width=True):
                    with st.spinner("Analyzing worker PPE and site hazards..."):
                        res, is_l, msg = execute_safety_audit(img_b, "image/jpeg", st.session_state.api_key, s_id)
                        st.session_state.safety_results = (res, is_l, msg)

            if st.session_state.safety_results:
                res, is_l, msg = st.session_state.safety_results
                render_safety_audit_view(res, is_l, msg)
        else:
            st.info("👆 Please upload a photo or click **'Load Sample Capture'** to run the safety audit.")

    with t2:
        st.subheader("🔍 Crack Diagnostics & Structural Integrity")
        c1, c2 = st.columns([1.2, 0.8])
        with c1:
            c_file = st.file_uploader("Upload Concrete / Defect Photo (JPG / PNG)", type=["jpg", "jpeg", "png"], key="crack_up")
        with c2:
            c_choice = st.selectbox("Or Test with Pre-Loaded Defect Sample", ["Sample 1: Transfer Girder Shear Fracture", "Sample 2: Cantilever Slab Spalling"], key="crack_choice")
            c_id = "sample_1" if "Sample 1" in c_choice else "sample_2"
            load_c = st.button("📥 Load Defect Sample", use_container_width=True, key="load_crack_btn")

        crk_b = None
        if c_file:
            crk_b = c_file.getvalue()
        elif load_c or "act_crack_b" in st.session_state:
            if load_c:
                st.session_state.act_crack_b = get_sample_image_bytes("crack", c_id)
                st.session_state.act_crack_id = c_id
                st.session_state.crack_results = None
            crk_b = st.session_state.get("act_crack_b")
            c_id = st.session_state.get("act_crack_id", "sample_1")

        if crk_b:
            cic1, cic2 = st.columns([1, 1.2])
            with cic1:
                st.image(crk_b, caption="Active Defect Telemetry", use_container_width=True)
            with cic2:
                if st.button("🔬 Execute Defect Diagnostics", key="run_c_diag", use_container_width=True):
                    with st.spinner("Classifying defect and estimating crack width..."):
                        c_res, c_is_l, c_msg = execute_crack_diagnostics(crk_b, "image/jpeg", st.session_state.api_key, c_id)
                        st.session_state.crack_results = (c_res, c_is_l, c_msg)

            if st.session_state.crack_results:
                c_res, c_is_l, c_msg = st.session_state.crack_results
                render_crack_diagnostics_view(c_res, c_is_l, c_msg)
        else:
            st.info("👆 Please upload a defect photo or click **'Load Defect Sample'**.")

    with t3:
        render_valuation_planner_view()

    with t4:
        render_weather_assistant_view(api_key=st.session_state.api_key)


if __name__ == "__main__":
    main()
