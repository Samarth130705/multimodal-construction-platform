# Multimodal Construction Intelligence Platform
### Skill Wallet Capstone Project 1

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-amber.svg)](https://opensource.org/licenses/MIT)
[![OSHA 1926](https://img.shields.io/badge/Standard-OSHA%2029%20CFR%201926-green.svg)](https://www.osha.gov/laws-regs/regulations/standardnumber/1926)
[![IS 456:2000](https://img.shields.io/badge/Standard-IS%20456%3A2000-orange.svg)](https://standardsbis.bsbedge.com/)

A turnkey, production-ready civil engineering and construction site intelligence platform built with Python, Streamlit, and Google Gemini Multimodal Vision models. Designed for 1-click deployment on Streamlit Community Cloud with zero external database dependencies.

---

## 🏛️ Platform Architecture Overview

```
                          ┌──────────────────────────────────────────────┐
                          │    Multimodal Construction Intelligence      │
                          │        Platform (Streamlit Cloud)            │
                          └──────────────────────┬───────────────────────┘
                                                 │
                   ┌─────────────────────────────┼─────────────────────────────┐
                   │                             │                             │
        ┌──────────▼──────────┐       ┌──────────▼──────────┐       ┌──────────▼──────────┐
        │  Gemini Vision API  │       │ Civil Engine & Math │       │   Generative AI     │
        │ (Multimodal Visual) │       │ (IS 456 / CPWD DSR) │       │ (Pollinations Flux) │
        └──────────┬──────────┘       └──────────┬──────────┘       └──────────┬──────────┘
                   │                             │                             │
    ┌──────────────┴──────────────┐              │                             │
    │                             │              │                             │
┌───▼────────────────┐   ┌────────▼─────────┐    │                             │
│ Tab 1: PPE Audit   │   │ Tab 2: Cracks    │    │                             │
│ OSHA 1926 & IS 456 │   │ Structural Shear │    │                             │
│ Safety Score 0-100 │   │ Defect Grouting  │    │                             │
└───┬────────────────┘   └────────┬─────────┘    │                             │
    │                             │              │                             │
    └──────────────┬──────────────┘              │                             │
                   │                             │                             │
        ┌──────────▼─────────────────────────────▼──────────┐       ┌──────────▼──────────┐
        │  Tab 4: Weather Alerts & Daily Site Assistant     │       │ Tab 3: Planning &   │
        │  - High Wind crane lockout                        │       │ Real Estate Val.    │
        │  - 42°C hot weather concrete curing protocols     │       │ - Material BOQ      │
        │  - Multi-turn SiteSenior AI Chatbot               │       │ - 3D Renderings     │
        └───────────────────────────────────────────────────┘       └─────────────────────┘
```

---

## 🚀 Key Modules & Capabilities

### 1. Sidebar & Secure Authentication
- **Secure Gemini Key Input**: Password-masked input field with support for `os.environ["GEMINI_API_KEY"]` or `st.secrets["GEMINI_API_KEY"]`.
- **Graceful Demonstration Fallback**: If no API key is supplied, the platform automatically switches to a high-fidelity **Demonstration Mode** using pre-configured synthetic telemetry and engineering simulations. Zero crash guarantee.
- **Standards & System Telemetry**: Live status of connected models, regulatory codes, and dependencies.

### 2. Tab 1 - Site Safety & PPE Audit (Epic 2)
- **Multimodal Visual Inspection**: Drag-and-drop file uploader (JPG/PNG) plus pre-loaded site capture samples.
- **Regulatory Frameworks**: OSHA 29 CFR 1926 (Construction Safety) & IS 456 / IS 2925 (Indian Standards).
- **Automated Detection Checklist**:
  - Hard hats & chinstrap compliance (OSHA 1926.100 / IS 2925)
  - High-visibility reflective vests & jackets (OSHA 1926.201 / EN ISO 20471)
  - Steel-toe puncture-resistant boots (OSHA 1926.96 / IS 15298)
  - Fall arrest harnesses and double-lanyard anchors (OSHA 1926.502 / IS 3521)
  - Eye, face, and respiratory shields (OSHA 1926.102 / IS 8521)
- **Interactive Outputs**:
  - `safety_score` (0-100) with dynamic color-coded metric cards.
  - Overall status badges (`Compliant`, `Warning - Action Required`, `Critical Non-Compliance`).
  - Identified site hazards with severity tags (`Low`, `Medium`, `High`, `Critical`) and explicit corrective engineering remedies.
  - Downloadable structured JSON report and Markdown executive summary.

### 3. Tab 2 - Crack Diagnostics & Structural Integrity (Epic 2)
- **Defect Classification Engine**:
  - Hairline Cracks (< 0.2 mm)
  - Settlement Cracks (0.3 - 2.0 mm)
  - Structural Shear Cracks (45° diagonal fractures near supports)
  - Thermal Expansion / Contraction Cracks
  - Concrete Spalling & Rebar Delamination (> 3.0 mm + oxidized steel)
- **Engineering Analytics**:
  - Estimated crack width in millimeters (mm) benchmarked against IS 456 permissible crack limits (0.3mm for mild exposure, 0.2mm for severe exposure).
  - Root cause deduction (shear overload, improper stirrup spacing, carbonation rust).
  - Step-by-step engineering rehabilitation specifications (low-pressure epoxy grouting per ASTM C881, structural CFRP U-jackets, Polymer Modified Mortar patching).
  - Downloadable forensic diagnostic telemetry (JSON & Markdown).

### 4. Tab 3 - Planning & Real Estate Valuation (Epic 3)
- **Interactive Multi-Variable Planning**:
  - **Structure Typologies**: High-Rise Residential (RCC Mivan), Grade-A Commercial Tech Park, Industrial PEB Warehouse, Luxury Villa Estate, Mixed-Use Commercial.
  - **Location Tiers**: Tier 1 (Mumbai, Delhi-NCR, Bengaluru), Tier 2 (Pune, Ahmedabad, Chandigarh), Tier 3 (Emerging Industrial Clusters).
  - **Built-up Area & Finish Multipliers**: Standard, Premium, and Ultra-Luxury finishing grades.
  - **Completion Progress Slider**: 0% to 100% stage-gate tracking.
- **Financial & Quantity Surveying Metrics**:
  - Total Estimated Project Budget & Rate per sqft in INR.
  - Capital Expenditure (CapEx) incurred to date (Lakhs & Crores).
  - Real estate market asset valuation reflecting land share equity and construction value-add.
  - Core materials BOQ: Fe550 TMT Rebar (MT), OPC/PPC Cement (Bags & MT), M-Sand, and Coarse Aggregate.
  - Milestone Progress Bar mapping to foundation, RCC superstructure, MEP, and finishes.
- **Generative 3D Architectural Rendering**:
  - Dynamic integration with Pollinations AI prompt generator.
  - Automatically synthesizes photorealistic 8K perspectives with customized lighting (Sunset Golden Hour, Blue Hour Twilight, Crisp Daylight) and architectural styling.

### 5. Tab 4 - Daily Site Assistant & Weather-Aware Advisory (Epic 5)
- **Weather Condition Selector**:
  - `High Wind (>40 km/h / Gale Warning)`: Crane hoisting lockout, slewing brake disengagement (OSHA 1926.1431), scaffolding evacuation.
  - `Heavy Rain / Monsoon Storm`: Excavation shoring stability (IS 3764), basement submersible dewatering, temporary 415V electrical board lockout.
  - `Extreme Heat (>42°C / Heatwave Alert)`: Hot-weather concreting protocol (IS 456 Cl. 13.5), ice-water batching (<32°C), aliphatic evaporation retarders, continuous 14-day wet ponding, worker hydration cycles.
  - `Cold Wave / Dense Fog (<8°C)`: Extended formwork striking periods (IS 456 Cl. 11.3), perimeter high-mast floodlighting.
  - `Normal / Clear Weather`: Standard full-speed operations.
- **Interactive Engineering Chatbot (SiteSenior AI)**:
  - Multi-turn chat assistant maintaining conversational context.
  - Specialized in IS codes, concrete mix designs, contractor billing, and safety procedures.
  - One-click quick inquiry chips for rapid field guidance.

---

## 🛠️ Local Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/multimodal-construction-intelligence.git
cd multimodal-construction-intelligence
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Configure Gemini API Key
You can pass the API key via environment variable:
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="AIzaSyYourGeminiApiKeyHere"

# Linux / macOS
export GEMINI_API_KEY="AIzaSyYourGeminiApiKeyHere"
```
*Or simply enter the key in the sidebar of the running app!*

### 5. Run the Streamlit Application
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501`.

---

## ☁️ 1-Click Deployment on Streamlit Community Cloud

1. Push this project folder to your GitHub repository.
2. Sign in to [share.streamlit.io](https://share.streamlit.io/).
3. Click **"New app"**, select your repository, branch (`main`), and set the main file path to:
   ```
   app.py
   ```
4. (Optional) Add your Gemini API key in **Advanced Settings -> Secrets**:
   ```toml
   GEMINI_API_KEY = "AIzaSyYourGeminiApiKeyHere"
   ```
5. Click **"Deploy"**! The application will build and launch in under 2 minutes.

---

## 📚 Standard Regulatory References

| Standard Code | Publishing Body | Scope |
| :--- | :--- | :--- |
| **OSHA 29 CFR 1926** | Occupational Safety and Health Admin (US) | Safety and health regulations for construction personnel, scaffolding, PPE, and cranes. |
| **IS 456:2000** | Bureau of Indian Standards (BIS) | Code of practice for plain and reinforced concrete (durability, crack width limits, curing, formwork removal). |
| **IS 875 (Parts 1–5)** | Bureau of Indian Standards (BIS) | Code of practice for design loads (dead, imposed, wind, snow) for buildings and structures. |
| **IS 3764:1992** | Bureau of Indian Standards (BIS) | Safety code for excavation work and trench shoring. |
| **CPWD DSR 2023/24** | Central Public Works Dept (Govt. of India) | Schedule of Rates for civil construction, materials, and labor analysis. |
| **ICRI 310.1R** | International Concrete Repair Institute | Surface preparation and structural concrete restoration guidelines. |

---

## 📄 License
Released under the [MIT License](LICENSE). Developed for the Skill Wallet Capstone Project.

