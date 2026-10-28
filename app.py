"""
Multimodal Construction Intelligence Platform
Skill Wallet Capstone Project 1

Production-grade Streamlit application integrating Google Gemini Multimodal Vision,
OSHA 1926 & IS 456 compliance, structural forensic diagnostics, real estate valuation,
and weather-triggered construction site advisories.
"""
import io
import os
import streamlit as st
from PIL import Image

# Set page config FIRST before any other Streamlit commands
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import modular application components
from modules.gemini_client import GENAI_AVAILABLE
from modules.safety_audit import execute_safety_audit, render_safety_audit_view
from modules.crack_diagnostics import execute_crack_diagnostics, render_crack_diagnostics_view
from modules.valuation_planner import render_valuation_planner_view
from modules.weather_assistant import render_weather_assistant_view
from modules.sample_assets import get_sample_image_bytes

# Custom Modern CSS Styling
CUSTOM_CSS = """
<style>
    /* Main Theme Overrides */
    .stApp {
        background: linear-gradient(135deg, #0B0F19 0%, #111827 50%, #0F172A 100%);
        color: #F8FAFC;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Metric Cards */
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

    /* Status Pills */
    .status-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Tabs Header */
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

    /* Header Banner */
    .header-box {
        background: linear-gradient(90deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-left: 6px solid #F59E0B;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 24px;
    }

    /* Buttons */
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


def init_session_state():
    """Initializes persistent application session state variables."""
    if "api_key" not in st.session_state:
        # Check environment or secrets
        st.session_state.api_key = os.environ.get("GEMINI_API_KEY", "")
    if "safety_results" not in st.session_state:
        st.session_state.safety_results = None
    if "crack_results" not in st.session_state:
        st.session_state.crack_results = None


def render_sidebar():
    """Renders the comprehensive sidebar with API management and platform architecture."""
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center; margin-bottom: 16px;">
                <span style="font-size: 2.4rem;">🏗️</span>
                <div style="font-size: 1.15rem; font-weight: 800; color: #F59E0B; letter-spacing: -0.02em;">
                    CONSTRUCTION INTELLIGENCE
                </div>
                <div style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em;">
                    Skill Wallet Capstone Project 1
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        # Google Gemini API Key Input
        st.subheader("🔑 Gemini API Configuration")
        user_key = st.text_input(
            "Google Gemini API Key",
            type="password",
            value=st.session_state.api_key,
            placeholder="AIzaSy...",
            help="Enter your Gemini API key for real-time multimodal vision inference (gemini-2.5-flash). If omitted, the platform seamlessly runs in high-fidelity Demonstration Mode."
        )

        if user_key != st.session_state.api_key:
            st.session_state.api_key = user_key

        # Mode Indicator Pill
        if st.session_state.api_key and len(st.session_state.api_key.strip()) > 10:
            st.markdown(
                """
                <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; 
                            border-radius: 6px; padding: 6px 12px; margin-top: 6px; text-align: center;">
                    <span style="color: #34D399; font-size: 0.82rem; font-weight: 700;">
                        🟢 LIVE API ACTIVE (Gemini 2.5 Flash)
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid #F59E0B; 
                            border-radius: 6px; padding: 6px 12px; margin-top: 6px; text-align: center;">
                    <span style="color: #FBBF24; font-size: 0.82rem; font-weight: 700;">
                        🟡 DEMONSTRATION MODE ACTIVE
                    </span>
                    <div style="color: #94A3B8; font-size: 0.72rem; margin-top: 2px;">
                        Full telemetry & realistic mock inference enabled without API key
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")

        # Architecture & Standard References
        st.subheader("🏛️ Regulatory Standards")
        st.markdown(
            """
            - **OSHA 29 CFR 1926**: Construction Safety
            - **IS 456:2000**: Plain & Reinforced Concrete
            - **IS 875 (Parts 1-3)**: Design Loads & Wind Codes
            - **IS 3764:1992**: Excavation Work Safety
            - **CPWD DSR 2023/24**: Rate Analysis Benchmarks
            - **ICRI 310.1R**: Concrete Repair Guidelines
            """
        )

        st.markdown("---")

        # Platform Specifications
        st.subheader("⚙️ System Telemetry")
        st.markdown(
            f"""
            - **Framework**: Streamlit 1.40+ (Cloud Native)
            - **Vision Engine**: Gemini 2.5 Flash (Multimodal)
            - **SDK Status**: `{'google-genai Connected' if GENAI_AVAILABLE else 'Direct Mock Fallback'}`
            - **3D Render Engine**: Pollinations AI (Flux)
            - **Database**: Zero-dependency stateless runtime
            """
        )

        st.markdown("---")
        st.caption("© 2026 Multimodal Construction Intelligence Platform | Capstone Project 1")


def main():
    init_session_state()
    render_sidebar()

    # Header Presentation Box
    st.markdown(
        """
        <div class="header-box">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                <div>
                    <h1 style="margin: 0; font-size: 2.1rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.02em;">
                        Multimodal Construction Intelligence Platform
                    </h1>
                    <div style="color: #F59E0B; font-size: 0.95rem; font-weight: 600; margin-top: 4px;">
                        Autonomous Site Safety Auditing • Forensic Structural Diagnostics • Real Estate Valuation • Daily Field Advisory
                    </div>
                </div>
                <div style="margin-top: 8px;">
                    <span style="background: rgba(245, 158, 11, 0.2); color: #FBBF24; border: 1px solid #F59E0B; 
                                padding: 6px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">
                        OSHA 1926 & IS 456 COMPLIANT
                    </span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 4 Core Tab Navigation
    tab1, tab2, tab3, tab4 = st.tabs([
        "🛡️ Site Safety & PPE Audit (Epic 2)",
        "🔍 Crack Diagnostics & Integrity (Epic 2)",
        "📐 Planning & Real Estate Valuation (Epic 3)",
        "🌤️ Daily Site Assistant & Weather Advisory (Epic 5)"
    ])

    # =========================================================================
    # TAB 1: SITE SAFETY & PPE AUDIT (EPIC 2)
    # =========================================================================
    with tab1:
        st.subheader("🛡️ Construction Site Safety & PPE Compliance Audit")
        st.caption("Automated multimodal computer vision inspection evaluating worker PPE compliance and physical site hazards against OSHA 1926 & IS 456 regulations.")

        # Input & File Upload Section
        u_col1, u_col2 = st.columns([1.2, 0.8])

        with u_col1:
            uploaded_safety_file = st.file_uploader(
                "Upload Construction Site Image (JPG / PNG)",
                type=["jpg", "jpeg", "png"],
                key="safety_uploader",
                help="Upload high-resolution photography from site drones, mobile cameras, or CCTV."
            )

        with u_col2:
            st.markdown("**Or Test with Pre-Loaded Telemetry Sample:**")
            sample_safety_choice = st.selectbox(
                "Select Test Scenario",
                options=[
                    "Sample 1: Active Rebar Framing & Scaffolding Deck (Mixed Compliance)",
                    "Sample 2: Deep Trench Excavation & Machinery Hazard (Critical Violations)"
                ],
                key="sample_safety_choice"
            )
            sample_id = "sample_1" if "Sample 1" in sample_safety_choice else "sample_2"
            use_sample = st.button("📥 Load Sample Site Capture", use_container_width=True)

        # Determine active image bytes
        image_bytes = None
        mime_type = "image/jpeg"

        if uploaded_safety_file is not None:
            image_bytes = uploaded_safety_file.getvalue()
            mime_type = uploaded_safety_file.type
        elif use_sample or "active_safety_bytes" in st.session_state:
            if use_sample:
                st.session_state.active_safety_bytes = get_sample_image_bytes("safety", sample_id)
                st.session_state.active_safety_id = sample_id
                st.session_state.safety_results = None # reset previous audit
            image_bytes = st.session_state.get("active_safety_bytes")
            sample_id = st.session_state.get("active_safety_id", "sample_1")

        if image_bytes is not None:
            img_col1, img_col2 = st.columns([1, 1.2])
            with img_col1:
                st.image(image_bytes, caption="Active Site Telemetry Capture", use_container_width=True)
            
            with img_col2:
                st.markdown("#### Ready for Multimodal Inspection")
                st.markdown(
                    """
                    This inspection analyzes:
                    - **Head Protection**: Hard hats & chinstraps (OSHA 1926.100 / IS 2925)
                    - **High-Visibility**: Reflective jackets/vests (OSHA 1926.201 / EN ISO 20471)
                    - **Foot Protection**: Steel-toe puncture-resistant boots (OSHA 1926.96 / IS 15298)
                    - **Fall Arrest**: Full-body harnesses & lifelines (OSHA 1926.502 / IS 3521)
                    - **Eye & Face**: Goggles & grinding shields (OSHA 1926.102 / IS 8521)
                    - **Site Hazards**: Edge barriers, loose rebar, electrical lines, housekeeping
                    """
                )
                
                if st.button("🚀 Execute Multimodal Safety & PPE Audit", key="run_safety_audit", use_container_width=True):
                    with st.spinner("Analyzing site imagery with multimodal neural models..."):
                        audit_data, is_live, msg = execute_safety_audit(
                            image_bytes=image_bytes,
                            mime_type=mime_type,
                            api_key=st.session_state.api_key,
                            sample_id=sample_id
                        )
                        st.session_state.safety_results = (audit_data, is_live, msg)

            if st.session_state.safety_results is not None:
                st.markdown("---")
                audit_data, is_live, msg = st.session_state.safety_results
                render_safety_audit_view(audit_data, is_live, msg)

        else:
            st.info("👆 Please upload a construction site photo or click **'Load Sample Site Capture'** to start auditing.")

    # =========================================================================
    # TAB 2: CRACK DIAGNOSTICS & STRUCTURAL INTEGRITY (EPIC 2)
    # =========================================================================
    with tab2:
        st.subheader("🔍 Crack Diagnostics & Concrete Structural Integrity")
        st.caption("Forensic computer vision defect classification, crack width estimation, root cause identification, and IS 456 & ACI 224 structural repair protocols.")

        c_col1, c_col2 = st.columns([1.2, 0.8])

        with c_col1:
            uploaded_crack_file = st.file_uploader(
                "Upload Concrete / Wall Defect Photo (JPG / PNG)",
                type=["jpg", "jpeg", "png"],
                key="crack_uploader",
                help="Upload close-up photos of cracked beams, columns, slab soffits, or masonry walls."
            )

        with c_col2:
            st.markdown("**Or Test with Pre-Loaded Defect Telemetry:**")
            sample_crack_choice = st.selectbox(
                "Select Structural Defect Scenario",
                options=[
                    "Sample 1: RC Transfer Girder 45° Shear Fracture (High Engineering Risk)",
                    "Sample 2: Cantilever Slab Soffit Spalling & Rebar Rust (Critical Defect)"
                ],
                key="sample_crack_choice"
            )
            crack_sample_id = "sample_1" if "Sample 1" in sample_crack_choice else "sample_2"
            use_crack_sample = st.button("📥 Load Sample Defect Capture", use_container_width=True)

        crack_image_bytes = None
        crack_mime = "image/jpeg"

        if uploaded_crack_file is not None:
            crack_image_bytes = uploaded_crack_file.getvalue()
            crack_mime = uploaded_crack_file.type
        elif use_crack_sample or "active_crack_bytes" in st.session_state:
            if use_crack_sample:
                st.session_state.active_crack_bytes = get_sample_image_bytes("crack", crack_sample_id)
                st.session_state.active_crack_id = crack_sample_id
                st.session_state.crack_results = None
            crack_image_bytes = st.session_state.get("active_crack_bytes")
            crack_sample_id = st.session_state.get("active_crack_id", "sample_1")

        if crack_image_bytes is not None:
            crk_col1, crk_col2 = st.columns([1, 1.2])
            with crk_col1:
                st.image(crack_image_bytes, caption="Active Defect Surface Telemetry", use_container_width=True)

            with crk_col2:
                st.markdown("#### Ready for Forensic Structural Analysis")
                st.markdown(
                    """
                    This diagnostic module evaluates:
                    - **Defect Typology**: Hairline, Settlement, Structural Shear, Thermal, Spalling
                    - **Dimensional Assessment**: Estimated crack width in millimeters (mm)
                    - **IS 456 Permissibility**: Compared against 0.3mm (mild) / 0.2mm (severe) limits
                    - **Root Cause Deduction**: Tensile overload, shear deficiency, carbonation rust
                    - **Rehabilitation Specifications**: Low-pressure epoxy grouting, CFRP wraps, PMM
                    """
                )

                if st.button("🔬 Execute Structural Defect Diagnostics", key="run_crack_diagnostics", use_container_width=True):
                    with st.spinner("Conducting forensic structural defect analysis..."):
                        crack_data, is_live_c, msg_c = execute_crack_diagnostics(
                            image_bytes=crack_image_bytes,
                            mime_type=crack_mime,
                            api_key=st.session_state.api_key,
                            sample_id=crack_sample_id
                        )
                        st.session_state.crack_results = (crack_data, is_live_c, msg_c)

            if st.session_state.crack_results is not None:
                st.markdown("---")
                crack_data, is_live_c, msg_c = st.session_state.crack_results
                render_crack_diagnostics_view(crack_data, is_live_c, msg_c)

        else:
            st.info("👆 Please upload a concrete defect photo or click **'Load Sample Defect Capture'** to initiate diagnostic inspection.")

    # =========================================================================
    # TAB 3: PLANNING & REAL ESTATE VALUATION (EPIC 3)
    # =========================================================================
    with tab3:
        render_valuation_planner_view()

    # =========================================================================
    # TAB 4: DAILY SITE ASSISTANT & WEATHER ADVISORY (EPIC 5)
    # =========================================================================
    with tab4:
        render_weather_assistant_view(api_key=st.session_state.api_key)


if __name__ == "__main__":
    main()

