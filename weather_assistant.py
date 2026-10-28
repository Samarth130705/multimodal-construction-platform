"""
Tab 4: Daily Site Assistant & Weather-Aware Advisory Module (Epic 5)
Provides real-time weather-induced construction protocols and an interactive multi-turn civil engineering assistant chatbot.
"""
from typing import Optional

try:
    import streamlit as st
except ImportError:
    st = None

from .gemini_client import run_gemini_chat

WEATHER_PROTOCOLS = {
    "High Wind (>40 km/h / Gale Warning)": {
        "alert_level": "CRITICAL OPERATIONAL ALERT",
        "badge_color": "#EF4444",
        "icon": "🌪️",
        "headline": "Crane Hoisting & Scaffolding Lockout Enforced",
        "protocols": [
            {
                "title": "Tower Crane & Hoist Suspension (OSHA 1926.1431 & IS 875)",
                "action": "Cease all tower crane, mobile crawler crane, and passenger hoist operations immediately. Disengage slewing brakes to permit free weather-vaning of crane jibs into wind axis."
            },
            {
                "title": "External Scaffolding & Suspended Cradles (IS 4014)",
                "action": "Evacuate external suspended working cradles. Latch and secure loose staging planks, green dust safety netting, and tarpaulin covers to structural ring pins."
            },
            {
                "title": "Loose Staging & Roofing Materials Lockdown",
                "action": "Tie down corrugated GI roofing sheets, lightweight aluminium formwork panels, and empty plastic chemical drums across all elevated slab decks."
            }
        ]
    },
    "Heavy Rain / Monsoon Storm": {
        "alert_level": "HIGH WEATHER ALERT",
        "badge_color": "#3B82F6",
        "icon": "🌧️",
        "headline": "Excavation Inundation & Electrical Isolation Protocol",
        "protocols": [
            {
                "title": "Trench & Foundation Berm Stability (IS 3764:1992)",
                "action": "Perform immediate geotech stability inspection of all deep basement excavation cuts. Deploy dual 15HP submersible de-watering pumps with standby diesel generators in lift pits."
            },
            {
                "title": "Temporary Electrical Isolation & ELCB Protection",
                "action": "De-energize temporary 415V distribution boxes in low-lying zones. Test all 30mA Earth Leakage Circuit Breakers (ELCB/RCCB) and elevate cables onto insulated support poles."
            },
            {
                "title": "Ban on Exposed Slab Concreting",
                "action": "Halt structural slab pours unless covered by rain-proof tarpaulin canopies. Rain on freshly screeded concrete destroys water-cement ratio, inducing severe surface spalling."
            }
        ]
    },
    "Extreme Heat (>42°C / Heatwave Alert)": {
        "alert_level": "SEVERE CLIMATIC ADVISORY",
        "badge_color": "#F97316",
        "icon": "🔥",
        "headline": "Concrete Hydration Retardation & Worker Heat Stress Controls",
        "protocols": [
            {
                "title": "Hot-Weather Concreting Protocol (IS 456 Cl. 13.5 & ACI 305R)",
                "action": "Maintain fresh concrete placement temp below 32°C using chilled batching water or flake ice. Apply aliphatic alcohol spray to prevent plastic shrinkage cracking."
            },
            {
                "title": "Continuous 14-Day Wet Curing Mandate",
                "action": "Enforce continuous wet hessian burlap ponding on all slabs and columns for minimum 14 days (Clause 13.5.2) to prevent tensile thermal micro-fissuring."
            },
            {
                "title": "Worker Shift Restructuring & Hydration Shifts",
                "action": "Shift heavy rebar binding and concreting to early morning (5:00 AM – 10:30 AM) and twilight hours. Mandate 15-minute shaded hydration breaks per hour with electrolyte ORS stations."
            }
        ]
    },
    "Cold Wave / Dense Fog (<8°C / Low Visibility)": {
        "alert_level": "MODERATE OPERATIONAL ADVISORY",
        "badge_color": "#A855F7",
        "icon": "❄️",
        "headline": "Delayed Formwork Stripping & Access Illumination",
        "protocols": [
            {
                "title": "Extended Formwork Deshuttering Times (IS 456 Cl. 11.3)",
                "action": "Concrete strength gain is significantly retarded below 10°C. Extend prop removal schedules by 30-50% and verify compressive cube strength exceeds 75% before striking."
            },
            {
                "title": "High-Mast Safety Lighting & Anti-Fog Gear",
                "action": "Activate perimeter floodlights. Mandate Class 3 fluorescent orange coats for ground personnel in transit corridors."
            }
        ]
    },
    "Normal / Clear Weather": {
        "alert_level": "STANDARD OPERATING CONDITIONS",
        "badge_color": "#10B981",
        "icon": "☀️",
        "headline": "Full-Speed Construction Operations Under Standard OSHA Compliance",
        "protocols": [
            {
                "title": "Full Site Production Authorized",
                "action": "All structural superstructure concreting, crane hoisting, and facade finishing works approved at 100% capacity."
            },
            {
                "title": "Standard Daily PPE Enforcement",
                "action": "Verify 100% hard hat, high-vis vest, and steel-toe footwear compliance at morning tool-box talk."
            }
        ]
    }
}

SYSTEM_ENGINEERING_PROMPT = """
You are "SiteSenior AI", the Principal Resident Civil Engineer, Forensic Structural Specialist, and Lead Safety Auditor on a major infrastructure and high-rise construction project.
You have comprehensive knowledge of:
1. Bureau of Indian Standards (BIS): IS 456:2000 (Plain and Reinforced Concrete), IS 800:2007 (Steel Structures), IS 1893 (Seismic Design), IS 875 (Design Loads - Wind & Imposed), IS 1200 (Method of Measurement of Building Works), IS 3764 (Excavation Safety).
2. OSHA 29 CFR 1926 (Safety and Health Regulations for Construction).
3. Concrete mix design (M20, M25, M30, M40, M60), slump tolerances, admixtures, and curing regimens.
4. Construction planning, CPM/PERT scheduling, quantity surveying, and contractor billing.

Always respond in a professional, practical, engineering-precise manner. Use clear markdown formatting, bullet points, and reference exact IS Code clauses or OSHA regulations where applicable.
"""

def render_weather_assistant_view(api_key: Optional[str] = None):
    """
    Renders Tab 4: Dynamic weather alerts and multi-turn engineering chatbot.
    """
    st.subheader("🌤️ Weather-Aware Daily Site Advisory & Safety Protocols")
    st.caption("Real-time climate-triggered operational mandates complying with OSHA 1926, IS 875 (Wind Loads), and IS 456 (Extreme Weather Concreting).")

    # Weather Selector Dropdown
    selected_weather = st.selectbox(
        "⚡ Current Environmental & Weather Condition at Site",
        options=list(WEATHER_PROTOCOLS.keys()),
        index=0
    )

    weather_info = WEATHER_PROTOCOLS[selected_weather]
    badge_col = weather_info["badge_color"]

    # Dynamic Alert Banner
    st.markdown(
        f"""
        <div style="background: rgba(30, 41, 59, 0.8); border: 2px solid {badge_col}; 
                    border-radius: 12px; padding: 18px 22px; margin-bottom: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 1.5rem;">{weather_info['icon']}</span>
                <span style="background: {badge_col}; color: #0F172A; font-weight: 800; font-size: 0.8rem; 
                            padding: 4px 12px; border-radius: 20px; text-transform: uppercase;">
                    {weather_info['alert_level']}
                </span>
            </div>
            <div style="font-size: 1.3rem; font-weight: 800; color: #F8FAFC; margin-bottom: 4px;">
                {weather_info['headline']}
            </div>
            <div style="font-size: 0.85rem; color: #94A3B8;">
                Triggered condition: <b>{selected_weather}</b>. All site supervisors and sub-contractors must implement the following mandatory controls immediately:
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Protocols Cards
    p_cols = st.columns(len(weather_info["protocols"]))
    for idx, proto in enumerate(weather_info["protocols"]):
        with p_cols[idx]:
            st.markdown(
                f"""
                <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); 
                            border-top: 3px solid {badge_col}; border-radius: 8px; padding: 14px; height: 100%;">
                    <div style="font-weight: 700; color: #F1F5F9; font-size: 0.92rem; margin-bottom: 8px;">
                        {proto['title']}
                    </div>
                    <div style="color: #CBD5E1; font-size: 0.82rem; line-height: 1.45;">
                        {proto['action']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # Interactive Construction Engineering Assistant Chatbot
    st.subheader("💬 SiteSenior AI: Lead Resident Civil Engineer & Safety Assistant")
    st.caption("Multi-turn conversation with specialized civil engineering reasoning. Ask about IS codes, mix designs, formwork, or safety procedures.")

    # Initialize chat state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {
                "role": "model",
                "content": (
                    "**Greetings Engineer.** I am **SiteSenior AI**, your lead resident civil engineer and safety compliance advisor. "
                    "I am standing by to assist with structural diagnostics, IS 456 / OSHA interpretations, concrete mix adjustments, "
                    "weather contingency plans, or contractor daily logs. How can I assist your site operations today?"
                )
            }
        ]

    # Quick prompt chips
    st.markdown("**Quick Inquiries:**")
    q1, q2, q3, q4 = st.columns(4)
    quick_query = None

    with q1:
        if st.button("⏱️ Formwork Stripping Times", use_container_width=True):
            quick_query = "What are the mandatory minimum formwork stripping periods for slabs and beams according to IS 456:2000 Clause 11.3?"
    with q2:
        if st.button("🏗️ Tower Crane Wind Limit", use_container_width=True):
            quick_query = "At what wind speed must tower crane operations be halted under OSHA and Indian safety standards?"
    with q3:
        if st.button("🔥 42°C Hot Concreting", use_container_width=True):
            quick_query = "How do I mitigate plastic shrinkage cracking when pouring concrete in extreme 42°C summer heat?"
    with q4:
        if st.button("💉 Structural Epoxy Injection", use_container_width=True):
            quick_query = "What is the step-by-step procedure and ASTM specification for pressure epoxy grouting a 1.5mm shear crack?"

    # Display chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_messages:
            role = msg["role"]
            avatar = "👷‍♂️" if role == "user" else "🤖"
            with st.chat_message(role, avatar=avatar):
                st.markdown(msg["content"])

    # User input
    user_input = st.chat_input("Ask a civil engineering or site safety question...")
    
    # Process if either quick_query clicked or user submitted text
    prompt_to_send = quick_query or user_input

    if prompt_to_send:
        # Append user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt_to_send})
        
        # Display immediately in chat
        with st.chat_message("user", avatar="👷‍♂️"):
            st.markdown(prompt_to_send)

        # Contextual prompt injecting current weather
        context_with_weather = (
            f"{SYSTEM_ENGINEERING_PROMPT}\n"
            f"Active Site Weather Condition: {selected_weather}.\n"
            f"Active Alert Level: {weather_info['alert_level']}."
        )

        with st.chat_message("model", avatar="🤖"):
            with st.spinner("SiteSenior AI is computing structural standards..."):
                reply = run_gemini_chat(
                    history=st.session_state.chat_messages[:-1],
                    user_message=prompt_to_send,
                    system_context=context_with_weather,
                    api_key=api_key
                )
                st.markdown(reply)

        # Append model message
        st.session_state.chat_messages.append({"role": "model", "content": reply})

    # Clear chat button
    c_left, c_right = st.columns([0.8, 0.2])
    with c_right:
        if st.button("🗑️ Reset Chat History", use_container_width=True):
            st.session_state.chat_messages = [
                {
                    "role": "model",
                    "content": "Chat history cleared. How may I assist your engineering tasks?"
                }
            ]
            st.rerun()
