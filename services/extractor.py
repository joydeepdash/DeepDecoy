def extract_intel(message: str):
    intel = {}

    if "bank" in message.lower():
        intel["financial_reference"] = True

    return intel
