from models.request import IncomingMessage
from core.session import get_session
from core.strategy import decide_next_state
from services.analyzer import analyze_message
from services.responder import generate_response
from services.extractor import extract_intel
from services.intel_agent import plan_next_intel
import time
from services.callback import send_callback
import asyncio
from core.config import FINAL_CALLBACK_URL
from fastapi import APIRouter, Header, HTTPException, Depends
from core.config import get_api_key



def build_agent_notes(session):
    notes = []

    intel = session.extracted_intel

    if intel.get("suspiciousKeywords"):
        notes.append("Urgency or manipulation language detected")

    if intel.get("phishingLinks"):
        notes.append("Suspicious link shared")

    if intel.get("upiIds") or intel.get("bankAccounts"):
        notes.append("Payment redirection attempt detected")

    if intel.get("phoneNumbers"):
        notes.append("External contact number shared")

    if session.last_scores.get("scam_confidence", 0) > 0.7:
        notes.append("High scam confidence based on conversation pattern")

    if not notes:
        notes.append("Scam interaction completed with limited intelligence signals")

    return "; ".join(notes)



def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key.strip() != get_api_key():
        raise HTTPException(status_code=401, detail="Invalid API key")


router = APIRouter()
DEBUG = False


@router.post("/message")
async def handle_message(
    req: IncomingMessage,
    _: None = Depends(verify_api_key)
):


    start_time = time.time()

    # 1️⃣ Load session
    session = get_session(req.sessionId)

    # 2️⃣ Store incoming message first
    session.history.append({
        "role": "user",
        "content": req.message.text
    })

    # 3️⃣ Decide next strategy using LLM
    decision = await decide_next_state(session)

    session.state = decision.next_state
    session.turns += 1

    # ---- TERMINATION OVERRIDE ----
    intel_categories_collected = sum(
        1 for v in session.extracted_intel.values() if v
    )

    if (
        intel_categories_collected >= 3
        or session.turns >= 8
        or decision.intel_score >= 0.7
    ):
        session.state = "terminate"


    # 4️⃣ Store decision scores for visibility/debugging
    session.last_scores = {
        "scam_confidence": decision.scam_confidence,
        "intel_score": decision.intel_score,
        "engagement_score": decision.engagement_score
    }

    # 5️⃣ Intelligence planning (NEW — lightweight step)
    intel_plan = await plan_next_intel(req.message.text, session.state)

    # 6️⃣ Generate response based on current state + intel goal
    analysis = await analyze_message(
        req.message.text,
        session.state,
        intel_plan
    )

    response = await generate_response(analysis)

    # 7️⃣ Extract intelligence
    intel = extract_intel(req.message.text)
    for key, values in intel.items():
        if key not in session.extracted_intel:
            session.extracted_intel[key] = []

        session.extracted_intel[key] = list(
            set(session.extracted_intel[key] + values)
        )


    # 8️⃣ Store assistant response
    session.history.append({
        "role": "assistant",
        "content": response
    })

    latency_ms = int((time.time() - start_time) * 1000)

    # 🔟 Send final callback when session terminates
    if session.state == "terminate" and not session.callback_sent:
        callback_payload = {
            "sessionId": session.session_id,
            "scamDetected": True,
            "totalMessagesExchanged": session.turns,
            "extractedIntelligence": session.extracted_intel,
            "agentNotes": build_agent_notes(session)
        }

        asyncio.create_task(
            send_callback(FINAL_CALLBACK_URL, callback_payload)
        )

        # prevent duplicate callbacks
        session.callback_sent = True

    

    # 9️⃣ Return structured result
    result = {
    "status": "success",
    "reply": response
    }

    if DEBUG:
        result.update({
            "state": session.state,
            "intel": session.extracted_intel,
            "scores": session.last_scores,
            "latency_ms": latency_ms
        })

    return result


@router.post("/test-callback")
async def test_callback(payload: dict):
    print("CALLBACK RECEIVED:", payload)
    return {"status": "received"}




