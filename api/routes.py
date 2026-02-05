from fastapi import APIRouter
from models.request import IncomingMessage
from core.session import get_session
from core.strategy import decide_next_state
from services.analyzer import analyze_message
from services.responder import generate_response
from services.extractor import extract_intel
from services.intel_agent import plan_next_intel

router = APIRouter()


@router.post("/message")
async def handle_message(req: IncomingMessage):

    # 1️⃣ Load session
    session = get_session(req.session_id)

    # 2️⃣ Store incoming message first
    session.history.append({
        "role": "user",
        "content": req.message
    })

    # 3️⃣ Decide next strategy using LLM
    decision = await decide_next_state(session)

    session.state = decision.next_state
    session.turns += 1

    # 4️⃣ Store decision scores for visibility/debugging
    session.last_scores = {
        "scam_confidence": decision.scam_confidence,
        "intel_score": decision.intel_score,
        "engagement_score": decision.engagement_score
    }

    # 5️⃣ Intelligence planning (NEW — lightweight step)
    intel_plan = await plan_next_intel(req.message, session.state)

    # 6️⃣ Generate response based on current state + intel goal
    analysis = await analyze_message(
        req.message,
        session.state,
        intel_plan
    )

    response = await generate_response(analysis)

    # 7️⃣ Extract intelligence
    intel = extract_intel(req.message)
    session.extracted_intel.update(intel)

    # 8️⃣ Store assistant response
    session.history.append({
        "role": "assistant",
        "content": response
    })

    # 9️⃣ Return structured result
    return {
        "reply": response,
        "state": session.state,
        "intel": session.extracted_intel,
        "scores": session.last_scores
    }
