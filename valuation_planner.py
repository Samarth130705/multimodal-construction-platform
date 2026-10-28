"""
Tab 3: Planning & Real Estate Valuation Module (Epic 3)
Calculates project budget, CapEx spent, asset valuation in INR, material bills of quantities,
and generates conceptual 3D architectural renders via Pollinations AI.
"""
import urllib.parse
from typing import Dict, Any, Tuple

try:
    import streamlit as st
except ImportError:
    st = None

STRUCTURE_SPECS = {
    "Residential High-Rise (RCC Mivan / Shear Wall)": {
        "tier1_rate": 2600,
        "tier2_rate": 2100,
        "tier3_rate": 1750,
        "steel_kg_sqft": 4.6,
        "cement_bags_sqft": 0.43,
        "sand_cft_sqft": 1.75,
        "coarse_cft_sqft": 2.85,
        "market_multiple": 3.6, # Ratio of completed market sales rate to base construction cost
        "render_desc": "luxurious contemporary high-rise residential apartment tower with glass balconies, landscaped podium, infinity pool, modern Indian skyline"
    },
    "Commercial Grade-A Office Complex": {
        "tier1_rate": 3600,
        "tier2_rate": 2900,
        "tier3_rate": 2300,
        "steel_kg_sqft": 5.4,
        "cement_bags_sqft": 0.49,
        "sand_cft_sqft": 1.90,
        "coarse_cft_sqft": 3.10,
        "market_multiple": 4.2,
        "render_desc": "state-of-the-art grade-A corporate tech park, parametric glass curtain facade, double-height grand lobby, biophilic atrium, commercial plaza"
    },
    "Industrial PEB Warehouse & Logistics Hub": {
        "tier1_rate": 1900,
        "tier2_rate": 1550,
        "tier3_rate": 1250,
        "steel_kg_sqft": 6.8,
        "cement_bags_sqft": 0.28,
        "sand_cft_sqft": 1.20,
        "coarse_cft_sqft": 2.10,
        "market_multiple": 2.2,
        "render_desc": "large modern pre-engineered industrial logistics warehouse, automated docking bays, solar roof panels, clean concrete apron, transport trucks"
    },
    "Luxury Villa / Premium Bungalow Estate": {
        "tier1_rate": 4500,
        "tier2_rate": 3600,
        "tier3_rate": 2900,
        "steel_kg_sqft": 4.9,
        "cement_bags_sqft": 0.46,
        "sand_cft_sqft": 1.85,
        "coarse_cft_sqft": 2.90,
        "market_multiple": 3.8,
        "render_desc": "minimalist tropical modern luxury villa, cantilevered wooden louvers, expansive travertine terrace, reflection pool, lush landscaped garden"
    },
    "Mixed-Use Commercial & Retail Mall": {
        "tier1_rate": 3300,
        "tier2_rate": 2650,
        "tier3_rate": 2150,
        "steel_kg_sqft": 5.1,
        "cement_bags_sqft": 0.45,
        "sand_cft_sqft": 1.80,
        "coarse_cft_sqft": 3.00,
        "market_multiple": 3.9,
        "render_desc": "dynamic mixed-use retail lifestyle center and urban plaza, illuminated storefronts, pedestrian promenade, modern architectural skylights"
    }
}

FINISH_MULTIPLIERS = {
    "Standard / Economy": 1.00,
    "Premium / Semi-Luxury": 1.25,
    "Ultra-Luxury / Bespoke High-End": 1.60
}

def format_inr(amount: float) -> Tuple[str, str]:
    """Formats raw INR into Lakhs and Crores for executive clarity."""
    if amount >= 10000000: # 1 Crore = 10,000,000
        crores = amount / 10000000
        return f"₹{crores:.2f} Cr", f"{crores:.2f} Crores"
    elif amount >= 100000: # 1 Lakh = 100,000
        lakhs = amount / 100000
        return f"₹{lakhs:.2f} L", f"{lakhs:.2f} Lakhs"
    else:
        return f"₹{amount:,.0f}", f"₹{amount:,.0f}"


def calculate_project_metrics(
    structure_type: str,
    built_up_sqft: float,
    tier: str,
    finish_grade: str,
    completion_pct: float
) -> Dict[str, Any]:
    """
    Computes CapEx, Current Asset Valuation, Material Quantities, and Milestone breakdown.
    """
    spec = STRUCTURE_SPECS[structure_type]
    finish_mult = FINISH_MULTIPLIERS[finish_grade]

    if "Tier 1" in tier:
        base_rate = spec["tier1_rate"]
        tier_label = "Tier 1 (Metro Prime)"
    elif "Tier 2" in tier:
        base_rate = spec["tier2_rate"]
        tier_label = "Tier 2 (Growth Center)"
    else:
        base_rate = spec["tier3_rate"]
        tier_label = "Tier 3 (Emerging Cluster)"

    effective_rate_per_sqft = base_rate * finish_mult
    total_project_budget = built_up_sqft * effective_rate_per_sqft
    capex_incurred = total_project_budget * (completion_pct / 100.0)
    capex_remaining = total_project_budget - capex_incurred

    # Real Estate Market Valuation
    # Completed market value = total budget * market multiple
    completed_market_value = total_project_budget * spec["market_multiple"]
    
    # Current stage valuation reflects land share (~35%), plus incurred CapEx, plus accrued developer margin
    land_component = total_project_budget * 0.40
    accrued_margin = (completed_market_value - total_project_budget - land_component) * (completion_pct / 100.0)
    
    # If completion is very low (<20%), apply an early-stage liquidity discount
    stage_factor = 0.90 if completion_pct < 25 else 1.00
    current_asset_valuation = (land_component + capex_incurred + max(0, accrued_margin)) * stage_factor

    # Materials Bill of Quantities (BOQ)
    total_steel_kg = built_up_sqft * spec["steel_kg_sqft"]
    total_steel_mt = total_steel_kg / 1000.0
    steel_incurred_mt = total_steel_mt * (completion_pct / 100.0)

    total_cement_bags = built_up_sqft * spec["cement_bags_sqft"]
    total_cement_mt = (total_cement_bags * 50) / 1000.0
    cement_incurred_bags = total_cement_bags * (completion_pct / 100.0)

    sand_cft = built_up_sqft * spec["sand_cft_sqft"]
    sand_tonnes = (sand_cft * 45) / 1000.0 # ~45 kg/cft

    coarse_cft = built_up_sqft * spec["coarse_cft_sqft"]
    coarse_tonnes = (coarse_cft * 48) / 1000.0 # ~48 kg/cft

    # Milestone identification
    if completion_pct <= 20:
        stage_name = "Substructure & Deep Foundation (Piling / Raft)"
        next_milestone = "RCC Superstructure Columns & Floor Slabs"
    elif completion_pct <= 55:
        stage_name = "RCC Superstructure Framing"
        next_milestone = "Masonry Walls, Plaster & MEP Rough-Ins"
    elif completion_pct <= 75:
        stage_name = "Masonry, MEP Conduit & Facade Glazing"
        next_milestone = "Internal Finishes, Flooring & Fixtures"
    elif completion_pct <= 90:
        stage_name = "Internal Architectural Finishes & External Development"
        next_milestone = "Testing, Commissioning, Fire NOC & Handover"
    else:
        stage_name = "Snagging, Commissioning & Handover"
        next_milestone = "Final Occupancy Certificate (OC) Delivery"

    return {
        "built_up_sqft": built_up_sqft,
        "effective_rate_per_sqft": effective_rate_per_sqft,
        "total_budget": total_project_budget,
        "capex_incurred": capex_incurred,
        "capex_remaining": capex_remaining,
        "completed_market_value": completed_market_value,
        "current_asset_valuation": current_asset_valuation,
        "completion_pct": completion_pct,
        "stage_name": stage_name,
        "next_milestone": next_milestone,
        "tier_label": tier_label,
        "materials": {
            "total_steel_mt": total_steel_mt,
            "steel_incurred_mt": steel_incurred_mt,
            "total_cement_bags": total_cement_bags,
            "cement_incurred_bags": cement_incurred_bags,
            "total_cement_mt": total_cement_mt,
            "sand_tonnes": sand_tonnes,
            "coarse_tonnes": coarse_tonnes
        },
        "render_desc": spec["render_desc"]
    }


def generate_pollinations_url(
    structure_type: str, 
    tier: str, 
    custom_keywords: str = "", 
    lighting: str = "Dramatic Sunset Golden Hour",
    seed: int = 42
) -> str:
    """
    Constructs an optimized Pollinations AI image generator URL for architectural rendering.
    """
    spec_desc = STRUCTURE_SPECS[structure_type]["render_desc"]
    clean_tier = tier.split(" - ")[0] if " - " in tier else tier
    
    prompt = (
        f"Hyperrealistic 8k architectural exterior photograph of a {spec_desc}, "
        f"located in {clean_tier} Indian metropolitan district, {lighting}, "
        f"photorealistic reflections, volumetric haze, cinematic composition, award-winning civil architecture"
    )
    if custom_keywords.strip():
        prompt += f", {custom_keywords.strip()}"

    encoded_prompt = urllib.parse.quote_plus(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=640&seed={seed}&nologo=true&enhance=true"


def render_valuation_planner_view():
    """
    Renders interactive inputs, budget cards, material quantities, and 3D architectural rendering.
    """
    st.subheader("🏗️ Project Financial Planning, CapEx & Real Estate Valuation")
    st.caption("Standardized CPWD DSR 2023/24 cost benchmarks, Indian city tier indices, and dynamic asset valuation.")

    # Input Controls Section
    with st.container():
        row1_col1, row1_col2 = st.columns([1.2, 1])

        with row1_col1:
            structure_type = st.selectbox(
                "🏢 Structure Typology",
                options=list(STRUCTURE_SPECS.keys()),
                index=0
            )

        with row1_col2:
            location_tier = st.selectbox(
                "📍 Location Tier & Cost Index",
                options=[
                    "Tier 1 - Mumbai, Delhi-NCR, Bengaluru, Hyderabad (1.0x Base)",
                    "Tier 2 - Pune, Ahmedabad, Kochi, Chandigarh, Jaipur (0.82x Base)",
                    "Tier 3 - Emerging Industrial Hubs & Smart Cities (0.68x Base)"
                ],
                index=0
            )

        row2_col1, row2_col2, row2_col3 = st.columns([1, 1, 1.2])

        with row2_col1:
            built_up_sqft = st.number_input(
                "📐 Built-Up Area (Sq.Ft.)",
                min_value=1000,
                max_value=2000000,
                value=75000,
                step=5000,
                help="Total built-up gross floor area including stilt/basements."
            )

        with row2_col2:
            finish_grade = st.selectbox(
                "✨ Specifications & Finishes",
                options=list(FINISH_MULTIPLIERS.keys()),
                index=1
            )

        with row2_col3:
            completion_pct = st.slider(
                "📊 Project Completion Progress (%)",
                min_value=0,
                max_value=100,
                value=45,
                step=5,
                help="Current physical progress stage-gate."
            )

    # Compute calculations
    metrics = calculate_project_metrics(
        structure_type, built_up_sqft, location_tier, finish_grade, completion_pct
    )

    budget_formatted, _ = format_inr(metrics["total_budget"])
    capex_formatted, _ = format_inr(metrics["capex_incurred"])
    valuation_formatted, _ = format_inr(metrics["current_asset_valuation"])
    completed_val_formatted, _ = format_inr(metrics["completed_market_value"])

    st.markdown("---")

    # Financial Metric Cards Row
    f1, f2, f3, f4 = st.columns(4)

    with f1:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 4px solid #3B82F6;">
                <div class="metric-label">Total Estimated Budget</div>
                <div class="metric-value" style="color: #60A5FA;">{budget_formatted}</div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">Rate: ₹{metrics['effective_rate_per_sqft']:,.0f} / sqft</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f2:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 4px solid #F59E0B;">
                <div class="metric-label">CapEx Incurred to Date</div>
                <div class="metric-value" style="color: #FBBF24;">{capex_formatted}</div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">{completion_pct}% of total budget spent</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f3:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 4px solid #10B981;">
                <div class="metric-label">Current Asset Valuation</div>
                <div class="metric-value" style="color: #34D399;">{valuation_formatted}</div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">Includes land share & accrued equity</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f4:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left: 4px solid #A855F7;">
                <div class="metric-label">Target Value on Delivery</div>
                <div class="metric-value" style="color: #C084FC;">{completed_val_formatted}</div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">Projected Gross Real Estate Value</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Milestone Progress Bar
    st.markdown("#### 🚩 Milestone Progress Tracker")
    st.progress(completion_pct / 100.0)
    
    col_stage, col_next = st.columns([1.2, 1])
    with col_stage:
        st.markdown(f"**Current Active Phase ({completion_pct}%):** `{metrics['stage_name']}`")
    with col_next:
        st.markdown(f"**Next Stage-Gate Milestone:** `{metrics['next_milestone']}`")

    st.markdown("---")

    # Materials Bill of Quantities (BOQ) & Steel / Cement Cards
    st.subheader("📦 Core Material Quantities (CPWD / IS 456 Benchmark Norms)")
    mat = metrics["materials"]

    m_col1, m_col2, m_col3, m_col4 = st.columns(4)

    with m_col1:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); 
                        border-radius: 8px; padding: 14px; text-align: center;">
                <div style="font-size: 0.8rem; color: #94A3B8; font-weight: 600;">Fe550 TMT REBAR STEEL</div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #38BDF8; margin: 4px 0;">{mat['total_steel_mt']:,.1f} MT</div>
                <div style="font-size: 0.75rem; color: #CBD5E1;">Incurred: {mat['steel_incurred_mt']:,.1f} MT</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m_col2:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); 
                        border-radius: 8px; padding: 14px; text-align: center;">
                <div style="font-size: 0.8rem; color: #94A3B8; font-weight: 600;">OPC / PPC CEMENT</div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #FBBF24; margin: 4px 0;">{mat['total_cement_bags']:,.0f} Bags</div>
                <div style="font-size: 0.75rem; color: #CBD5E1;">Equivalent: {mat['total_cement_mt']:,.1f} MT</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m_col3:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); 
                        border-radius: 8px; padding: 14px; text-align: center;">
                <div style="font-size: 0.8rem; color: #94A3B8; font-weight: 600;">RIVER / M-SAND</div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #F472B6; margin: 4px 0;">{mat['sand_tonnes']:,.0f} MT</div>
                <div style="font-size: 0.75rem; color: #CBD5E1;">Fine Aggregate Volume</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with m_col4:
        st.markdown(
            f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); 
                        border-radius: 8px; padding: 14px; text-align: center;">
                <div style="font-size: 0.8rem; color: #94A3B8; font-weight: 600;">COARSE AGGREGATE (10/20mm)</div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #A78BFA; margin: 4px 0;">{mat['coarse_tonnes']:,.0f} MT</div>
                <div style="font-size: 0.75rem; color: #CBD5E1;">Crushed Blue Metal</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    # Conceptual 3D Architectural Rendering via Pollinations AI
    st.subheader("🎨 Conceptual 3D Architectural Rendering (Pollinations AI Integration)")
    st.caption("Real-time generative AI rendering tailored to structure typology, metropolitan tier, and daylight aesthetics.")

    p_col1, p_col2 = st.columns([1, 1])

    with p_col1:
        lighting_style = st.selectbox(
            "🌅 Environmental Lighting Atmosphere",
            options=[
                "Dramatic Sunset Golden Hour with Volumetric Rays",
                "Crisp Blue-Sky Daylight with Sharp Architectural Shadows",
                "Atmospheric Twilight Blue Hour with Warm Interior Illuminations",
                "Moody Overcast Soft Diffuse Daylight"
            ],
            index=0
        )

    with p_col2:
        custom_prompt_add = st.text_input(
            "✏️ Additional Architectural Details (Optional)",
            value="LEED Platinum green terrace, floor-to-ceiling glass, water reflection",
            help="Add specific facade textures, greenery, or surrounding features."
        )

    # Generate Image Seed or URL
    render_seed = st.number_input("🎲 Seed (Change to regenerate variation)", min_value=1, max_value=999999, value=108, step=1)
    
    pollinations_url = generate_pollinations_url(
        structure_type, location_tier, custom_prompt_add, lighting_style, seed=render_seed
    )

    st.markdown(
        f"""
        <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(245, 158, 11, 0.3); 
                    border-radius: 12px; padding: 16px; margin: 16px 0; text-align: center;">
            <img src="{pollinations_url}" alt="Conceptual 3D Architectural Render" 
                 style="width: 100%; max-height: 520px; object-fit: cover; border-radius: 8px; 
                        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);" />
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px; font-size: 0.85rem; color: #94A3B8;">
                <span>AI Generator: <b>Pollinations Flux Architectural Engine</b></span>
                <a href="{pollinations_url}" target="_blank" style="color: #F59E0B; text-decoration: none; font-weight: 600;">
                    🔗 Open High-Res Render (1024x640)
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
