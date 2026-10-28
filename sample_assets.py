"""
Sample images and mock data generation for Demonstration Mode.
Provides realistic construction visuals and structural defect images.
"""
import io
import base64
from typing import Any, Optional

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

def create_synthetic_image(title: str, subtitle: str, color_scheme: str = "safety") -> Any:
    """Creates a high-contrast procedural synthetic construction photo placeholder."""
    if not PIL_AVAILABLE:
        return None

    width, height = 800, 500
    
    if color_scheme == "safety":
        bg_color = (25, 33, 44)
        accent_color = (245, 158, 11) # Safety Amber
        line_color = (71, 85, 105)
    elif color_scheme == "crack":
        bg_color = (38, 38, 38) # Concrete Grey
        accent_color = (239, 68, 68) # Warning Red
        line_color = (115, 115, 115)
    else:
        bg_color = (15, 23, 42)
        accent_color = (59, 130, 246)
        line_color = (51, 65, 85)

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Draw structural grid / scaffolding pattern
    for x in range(0, width, 50):
        draw.line([(x, 0), (x, height)], fill=line_color, width=1)
    for y in range(0, height, 50):
        draw.line([(0, y), (width, y)], fill=line_color, width=1)

    # Diagonal bracing lines
    draw.line([(0, 0), (width, height)], fill=line_color, width=2)
    draw.line([(0, height), (width, 0)], fill=line_color, width=2)

    # Draw simulated feature
    if color_scheme == "crack":
        # Draw realistic jagged crack line
        crack_points = [
            (150, 80), (220, 140), (290, 160), (360, 230), 
            (420, 250), (490, 320), (550, 360), (620, 420)
        ]
        draw.line(crack_points, fill=(15, 15, 15), width=7)
        draw.line(crack_points, fill=accent_color, width=2)
        # Minor fracture branch
        draw.line([(360, 230), (430, 210), (480, 225)], fill=(15, 15, 15), width=4)
        draw.line([(360, 230), (430, 210), (480, 225)], fill=accent_color, width=1)
    elif color_scheme == "safety":
        # Draw hazard boundary & worker silhouettes
        draw.rectangle([(200, 150), (600, 380)], outline=accent_color, width=3)
        # Danger hazard stripes on top
        for i in range(200, 600, 40):
            draw.line([(i, 150), (i + 20, 170)], fill=accent_color, width=4)

    # Header Banner Box
    draw.rectangle([(40, 30), (width - 40, 110)], fill=(15, 23, 42, 220), outline=accent_color, width=2)
    
    # Text (Use default font if TTF unavailable)
    draw.text((60, 45), f"SITE TELEMETRY CAPTURE // {title.upper()}", fill=(255, 255, 255))
    draw.text((60, 75), f"Standards: {subtitle} | Timecode: 10:42:18 IST", fill=accent_color)

    # Footer HUD box
    draw.rectangle([(40, height - 70), (width - 40, height - 25)], fill=(15, 23, 42, 220), outline=line_color, width=1)
    draw.text((60, height - 55), "AI VISION SENSOR: SONY IMX586 48MP | CALIBRATION: ACTIVE", fill=(148, 163, 184))

    return img

def get_sample_image_bytes(category: str, sample_id: str = "sample_1") -> bytes:
    """Returns PIL Image encoded as JPEG bytes for testing."""
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
        img = create_synthetic_image("Civil Engineering Inspection", "Inspection Telemetry", "default")
    
    if img is None:
        # Fallback 1x1 transparent GIF/JPEG bytes if PIL is unavailable
        return b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
    
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()

def get_mock_safety_data(scenario: str = "sample_1") -> dict:
    """Returns high-fidelity structured JSON simulation for PPE audit."""
    if scenario == "sample_2":
        return {
            "safety_score": 58,
            "overall_status": "Critical Non-Compliance",
            "workers_detected_count": 3,
            "compliance_summary": "High-risk violations detected in trench zone. 1 operative within 2.5m excavation zone without hard hat or perimeter lifeline anchor.",
            "ppe_detection": [
                {
                    "item": "Hard Hats / Safety Helmets",
                    "status": "Non-Compliant",
                    "detected_count": 1,
                    "expected_count": 3,
                    "compliance_rate": 33,
                    "standard": "OSHA 29 CFR 1926.100 / IS 2925",
                    "notes": "2 workers inside active excavation zone missing type-1 protective hard hats."
                },
                {
                    "item": "High-Visibility Safety Vests",
                    "status": "Partial",
                    "detected_count": 2,
                    "expected_count": 3,
                    "compliance_rate": 67,
                    "standard": "OSHA 1926.201 / EN ISO 20471 Class 2",
                    "notes": "1 worker wearing soiled non-reflective dark shirt adjacent to backhoe swing radius."
                },
                {
                    "item": "Steel-Toe Safety Footwear",
                    "status": "Compliant",
                    "detected_count": 3,
                    "expected_count": 3,
                    "compliance_rate": 100,
                    "standard": "OSHA 1926.96 / IS 15298 (Class 1)",
                    "notes": "Heavy-duty puncture-resistant steel toe safety boots confirmed for all personnel."
                },
                {
                    "item": "Trench Fall Arrest / Harness",
                    "status": "Non-Compliant",
                    "detected_count": 0,
                    "expected_count": 3,
                    "compliance_rate": 0,
                    "standard": "OSHA 1926.502 / IS 3521",
                    "notes": "No harness or retrieve lifeline tethering for personnel working within trench wall collapse perimeter."
                },
                {
                    "item": "Protective Gloves & Dust Masks",
                    "status": "Partial",
                    "detected_count": 1,
                    "expected_count": 3,
                    "compliance_rate": 33,
                    "standard": "OSHA 1926.102 / IS 8521",
                    "notes": "Workers handling sharp rebar rods without reinforced anti-cut mechanical gloves."
                }
            ],
            "site_hazards": [
                {
                    "hazard": "Trench Shoring & Unprotected Edge Hazard",
                    "severity": "Critical",
                    "location_zone": "Trench Perimeter Bay 2",
                    "regulatory_violation": "OSHA 1926.652 & IS 3764:1992",
                    "corrective_remedy": "Immediately withdraw personnel. Erect trench box shoring and hydraulic sheet piling before re-entry."
                },
                {
                    "hazard": "Excavator Swing Radius Struck-By Risk",
                    "severity": "High",
                    "location_zone": "Zone 1A Machinery Corridor",
                    "regulatory_violation": "OSHA 1926.600",
                    "corrective_remedy": "Demarcate 5-meter red exclusion zone with warning tape and assign dedicated banksman/flagman."
                },
                {
                    "hazard": "Missing Emergency Trench Egress Ladder",
                    "severity": "Medium",
                    "location_zone": "Deep Cut Sector B",
                    "regulatory_violation": "OSHA 1926.651(c)(2)",
                    "corrective_remedy": "Install structural access ladder extending minimum 3 ft above trench edge within 25 ft lateral travel."
                }
            ]
        }
    
    # Default scenario (sample_1)
    return {
        "safety_score": 84,
        "overall_status": "Warning - Action Required",
        "workers_detected_count": 4,
        "compliance_summary": "Good overall baseline compliance on rebar framing deck. 4/4 hard hats and safety boots verified. Fall arrest lanyard anchor violation noted at level 3 scaffolding perimeter.",
        "ppe_detection": [
            {
                "item": "Hard Hats / Safety Helmets",
                "status": "Compliant",
                "detected_count": 4,
                "expected_count": 4,
                "compliance_rate": 100,
                "standard": "OSHA 29 CFR 1926.100 / IS 2925",
                "notes": "100% compliance. All 4 operatives wearing chinstrap-secured industrial safety helmets."
            },
            {
                "item": "High-Visibility Safety Vests",
                "status": "Compliant",
                "detected_count": 4,
                "expected_count": 4,
                "compliance_rate": 100,
                "standard": "OSHA 1926.201 / EN ISO 20471 Class 2",
                "notes": "Fluorescent fluorescent yellow/orange retroreflective vests clearly visible."
            },
            {
                "item": "Steel-Toe Safety Footwear",
                "status": "Compliant",
                "detected_count": 4,
                "expected_count": 4,
                "compliance_rate": 100,
                "standard": "OSHA 1926.96 / IS 15298 (Class 1)",
                "notes": "Verified steel toe puncture-proof site boots."
            },
            {
                "item": "Fall Arrest Harness & Lifeline Anchor",
                "status": "Partial",
                "detected_count": 2,
                "expected_count": 4,
                "compliance_rate": 50,
                "standard": "OSHA 1926.502 / IS 3521",
                "notes": "2 workers at slab edge have harnesses worn, but secondary safety lanyard is unhooked from static lifeline."
            },
            {
                "item": "Eye & Face Protection",
                "status": "Partial",
                "detected_count": 2,
                "expected_count": 4,
                "compliance_rate": 50,
                "standard": "OSHA 1926.102 / IS 8521",
                "notes": "Operative rebar tie binding lacking ANSI Z87.1 impact-resistant wrap goggles."
            }
        ],
        "site_hazards": [
            {
                "hazard": "Unanchored Fall Arrest Lanyard at Perimeter",
                "severity": "High",
                "location_zone": "Level 3 Slab Edge Cantilever",
                "regulatory_violation": "OSHA 1926.501(b)(1) & IS 3521",
                "corrective_remedy": "Enforce 100% tie-off protocol immediately. Clip double-scaffold hooks to certified 8mm wire rope static line."
            },
            {
                "hazard": "Unprotected Impalement Hazard from Vertical Rebar Dowels",
                "severity": "Medium",
                "location_zone": "Bay 4 Column Starter Bars",
                "regulatory_violation": "OSHA 1926.701(b) & IS 456",
                "corrective_remedy": "Cap all exposed vertical steel rebar ends with OSHA-approved mushroom steel-reinforced rebar caps."
            },
            {
                "hazard": "Scattered Cable & Binding Wire Trip Hazard",
                "severity": "Low",
                "location_zone": "Deck Access Walkway",
                "regulatory_violation": "OSHA 1926.25 Housekeeping",
                "corrective_remedy": "Elevate temporary 3-phase power cables on insulated S-hooks and clear rebar scrap off deck."
            }
        ]
    }

def get_mock_crack_data(scenario: str = "sample_1") -> dict:
    """Returns high-fidelity structured JSON simulation for crack diagnostics."""
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
                "Delamination and complete shear spalling of concrete cover layer.",
                "Water seepage through unsealed tile joints on upper exposed deck."
            ],
            "engineering_repairs": [
                {
                    "step": 1,
                    "action": "Immediate Temporary Shoring",
                    "specification": "Install heavy-duty adjustable steel prop towers (Acro props) spaced at 1.0m center-to-center beneath the cantilever span."
                },
                {
                    "step": 2,
                    "action": "Chipping & Substrate Preparation",
                    "specification": "Chisel back sound concrete 20mm behind corroded rebar circumference per ICRI Technical Guideline No. 310.1R."
                },
                {
                    "step": 3,
                    "action": "Rebar De-Rusting & Passivation",
                    "specification": "Mechanical grit blast rebar to SA 2.5 white metal finish. Apply 2 coats of zinc-rich epoxy anti-corrosion primer (ASTM D520)."
                },
                {
                    "step": 4,
                    "action": "Polymer Modified Mortar Patching",
                    "specification": "Apply SBR bonding coat followed by structural low-shrinkage fiber-reinforced repair mortar (M40 grade equivalent)."
                },
                {
                    "step": 5,
                    "action": "CFRP Strengthening & Protective Coating",
                    "specification": "Wrap soffit with 300 gsm unidirectional Carbon Fiber Reinforced Polymer (CFRP) fabric saturated in structural epoxy resin."
                }
            ],
            "risk_assessment": {
                "load_capacity_reduction_pct": 35,
                "water_ingress_risk": "Severe",
                "monitoring_frequency": "Continuous until shoring and composite repair is commissioned"
            }
        }
    
    # Default scenario (sample_1 - Shear crack)
    return {
        "defect_type": "Structural Shear Crack",
        "estimated_crack_width_mm": 1.85,
        "severity_index": "High Engineering Risk",
        "urgency": "High Priority (Remediate within 7 days)",
        "structural_element": "Reinforced Concrete Transfer Girder (Near Support End)",
        "is_code_reference": "IS 456:2000 Clause 40 (Design for Shear) & Clause 43.1",
        "root_causes": [
            "Excessive principal tensile stress inclined at approximately 45 degrees near beam support.",
            "Inadequate shear reinforcement (stirrup spacing > 0.75d) for redistributed construction crane loads.",
            "Dynamic load amplification from heavy material staging directly above girder span.",
            "Differential deflection during progressive formwork de-shuttering."
        ],
        "engineering_repairs": [
            {
                "step": 1,
                "action": "Load Relieving & De-Staging",
                "specification": "Immediately clear all stacked bricks, rebar bundles, and wet mortar tubs from the top flange of the transfer girder."
            },
            {
                "step": 2,
                "action": "Surface Preparation & Port Installation",
                "specification": "V-groove crack to 15x15mm along full fracture path. Bond injection nipple packers at 200mm intervals using rapid epoxy putty."
            },
            {
                "step": 3,
                "action": "Low-Viscosity Epoxy Pressure Grouting",
                "specification": "Inject high-modulus, low-viscosity structural epoxy resin (ASTM C881 Type I/IV Grade 1) under 0.2 to 0.4 MPa pressure."
            },
            {
                "step": 4,
                "action": "External Shear Banding / CFRP U-Wraps",
                "specification": "Install dual-layer 450 gsm unidirectional Carbon Fiber U-jackets anchored into beam top flange to restore shear capacity."
            },
            {
                "step": 5,
                "action": "Acoustic / Optical Crack Gauge Monitoring",
                "specification": "Affix calibrated Tell-Tale polycarbonate crack displacement gauge (0.1mm vernier resolution) to monitor micro-movement."
            }
        ],
        "risk_assessment": {
            "load_capacity_reduction_pct": 22,
            "water_ingress_risk": "Moderate",
            "monitoring_frequency": "Every 48 hours until epoxy curing inspection test"
        }
    }
