"""
Gemini API Client with Graceful Demonstration Fallback.
Supports google-genai SDK, multimodal vision queries, and robust JSON parsing.
"""
import os
import json
import re
from typing import Optional, Tuple, Dict, Any

# Try importing google-genai SDK
try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


def clean_json_text(raw_text: str) -> str:
    """Extracts JSON substring from markdown code blocks or surrounding text."""
    # Look for ```json ... ``` block
    json_block = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, re.DOTALL)
    if json_block:
        return json_block.group(1).strip()
    
    # Alternatively find the outermost braces
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
    """
    Executes a multimodal vision inference call using Gemini.
    Returns: (is_live_call, parsed_json_or_none, status_message)
    """
    effective_key = api_key or os.environ.get("GEMINI_API_KEY", "").strip()
    
    if not effective_key:
        return False, None, "No Gemini API Key supplied. Demonstration Mode active."
    
    if not GENAI_AVAILABLE:
        return False, None, "google-genai SDK not available in environment. Running in Demo Mode."

    try:
        client = genai.Client(api_key=effective_key)
        
        # Prepare parts
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type
        )
        
        system_instruction = (
            "You are an expert civil and structural engineer and certified OSHA 1926 & IS 456 "
            "construction safety auditor. Always provide structured, engineering-accurate analysis. "
            "Always return your primary output in strict JSON format when requested."
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
        return False, None, f"Gemini API request failed: {str(e)}. Falling back to verified demonstration data."


def run_gemini_chat(
    history: list, 
    user_message: str, 
    system_context: str, 
    api_key: Optional[str] = None,
    model_name: str = "gemini-2.5-flash"
) -> str:
    """
    Executes interactive multi-turn civil engineering chat assistant.
    """
    effective_key = api_key or os.environ.get("GEMINI_API_KEY", "").strip()

    if not effective_key or not GENAI_AVAILABLE:
        # High quality rule-based response for demo mode
        return generate_demo_chat_reply(user_message, system_context)

    try:
        client = genai.Client(api_key=effective_key)
        
        # Convert history format
        formatted_contents = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            formatted_contents.append(
                types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
            )
        # Add current user message
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

    except Exception as e:
        demo_reply = generate_demo_chat_reply(user_message, system_context)
        return f"[Live API Notice: {str(e)}]\n\n(Fallback Advisory Response):\n{demo_reply}"


def generate_demo_chat_reply(user_message: str, system_context: str) -> str:
    """Generates an intelligent context-aware civil engineering answer during Demo Mode."""
    msg = user_message.lower()
    
    if "formwork" in msg or "stripping" in msg or "deshutter" in msg:
        return (
            "**Formwork Removal Minimum Periods (per IS 456:2000 Clause 11.3 & Table 1):**\n\n"
            "1. **Walls, columns, and vertical faces of all structural members**: 16 to 24 hours (with OPC).\n"
            "2. **Slab soffits (props left under)**: 3 days (props refixed immediately).\n"
            "3. **Beam soffits (props left under)**: 7 days.\n"
            "4. **Removal of props under slabs**:\n"
            "   - Spanning up to 4.5 m: 7 days\n"
            "   - Spanning over 4.5 m: 14 days\n"
            "5. **Removal of props under beams and arches**:\n"
            "   - Spanning up to 6 m: 14 days\n"
            "   - Spanning over 6 m: 21 days\n\n"
            "*Safety Alert*: In cold weather (<15°C) or when using blended cements (PPC/GGBS), extend these durations by 25-50% and verify concrete cube compressive strength exceeds 70% of characteristic target."
        )
    elif "crane" in msg or "wind" in msg or "lift" in msg:
        return (
            "**Tower Crane & Rigging Wind Safety Protocol (OSHA 1926.1431 & IS 875 Part 3):**\n\n"
            "- **Wind Speed < 32 km/h (9 m/s)**: Normal hoisting operations permitted with taglines.\n"
            "- **Wind Speed 32 - 38 km/h**: Cease hoisting large-surface panel loads (formwork shutters, glazing cassettes, precast slabs).\n"
            "- **Wind Speed > 38 km/h (10.5 m/s) / Gale Force**: Mandatory **STOP WORK** order. Disengage slewing brake to allow crane jib to weather-vane freely into the wind direction to avoid torsion failure.\n"
            "- **Inspection**: All hook latch interlocks and 100% ground exclusion zones must be barricaded."
        )
    elif "heat" in msg or "curing" in msg or "hot weather" in msg:
        return (
            "**Hot Weather Concreting Protocols (ACI 305R & IS 456:2000 Clause 13.5):**\n\n"
            "1. **Fresh Concrete Temperature**: Must not exceed 32°C (90°F) at point of discharge. Utilize chilled batching water or flake ice substitution.\n"
            "2. **Plastic Shrinkage Crack Prevention**: If evaporation rate exceeds 1.0 kg/m²/hr, apply aliphatic alcohol evaporation retarder spray immediately after screeding.\n"
            "3. **Admixtures**: Incorporate ASTM C494 Type D or Type G retarding plasticizers to maintain 90-minute slump retention.\n"
            "4. **Curing Regime**: Start wet hessian burlap covering as soon as concrete hardens sufficiently. Keep continuously ponded/wetted for minimum 14 days (IS 456 Cl. 13.5.2)."
        )
    elif "crack" in msg or "epoxy" in msg or "spall" in msg:
        return (
            "**Concrete Crack Remediation Matrix:**\n\n"
            "- **Hairline (<0.2 mm non-structural)**: Low-viscosity acrylic surface sealer or elastomeric micro-crack bridge.\n"
            "- **Active Structural Shear Cracks (>0.3 mm)**: Low-viscosity epoxy resin injection (ASTM C881 Type I, Grade 1) with staggered surface injection nipples under 0.2 to 0.4 MPa pressure.\n"
            "- **Water-Bearing Cracks**: Hydrophobic polyurethane (PU) expanding foam injection to arrest active hydrostatic head before secondary epoxy grouting.\n"
            "- **Rebar Delamination & Spall**: Break out concrete to 20mm behind rebar, mechanical wire brush to SA 2.5, coat with zinc-rich primer, and apply fiber-reinforced polymer modified mortar (PMM)."
        )
    else:
        return (
            f"**SiteSenior AI Advisory (IS 456 / OSHA 1926 Guideline):**\n\n"
            f"Regarding your query on *\"{user_message}\"*:\n\n"
            "1. **Structural Verification**: Review current site staging against approved GFC (Good-for-Construction) structural drawings and RFI clarifications.\n"
            "2. **Quality & Standard Compliance**: Verify batching tickets, slump cone tests (target 100-120mm for pumped concrete), and 7/28-day cube crushing registers (IS 516).\n"
            "3. **Site Safety Protocol**: Maintain clear pedestrian-vehicle segregation, check GFCI earth leakage circuit breakers on all temporary distribution boards, and inspect scaffolding green tags.\n\n"
            "*Recommendation*: For specialized engineering sign-off, verify calculations with the project structural consultant."
        )

