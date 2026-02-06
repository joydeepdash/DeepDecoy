import re
from typing import Dict, List

# --- REGEX PATTERNS ---

UPI_PATTERN = re.compile(
    r"\b[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}\b"
)

PHONE_PATTERN = re.compile(
    r"(?:\+91[-\s]?)?[6-9]\d{9}\b"
)

URL_PATTERN = re.compile(
    r"(https?://[^\s]+)"
)

# Very loose bank/account number detection
BANK_ACCOUNT_PATTERN = re.compile(
    r"\b\d{9,18}\b"
)

# Common scam urgency / manipulation keywords
SUSPICIOUS_KEYWORDS = {
    "urgent",
    "verify now",
    "account blocked",
    "account suspended",
    "limited time",
    "immediately",
    "otp",
    "upi",
    "refund",
    "kyc",
    "prize",
    "lottery",
    "click link",
    "update details",
}


# --- CORE FUNCTION ---

def extract_intel(message: str) -> Dict[str, List[str]]:
    """
    Extract scam intelligence from a single message.

    Stateless extraction:
    - Caller (session/service layer) should merge results across turns.
    """

    text = message.lower()

    intel = {
        "bankAccounts": [],
        "upiIds": [],
        "phishingLinks": [],
        "phoneNumbers": [],
        "suspiciousKeywords": [],
    }

    # --- UPI IDs ---
    upi_ids = UPI_PATTERN.findall(message)
    intel["upiIds"].extend(upi_ids)

    # --- Phone Numbers ---
    phones = PHONE_PATTERN.findall(message)
    intel["phoneNumbers"].extend(phones)

    # --- Links ---
    urls = URL_PATTERN.findall(message)
    intel["phishingLinks"].extend(urls)

    # --- Bank / Account Numbers ---
    accounts = BANK_ACCOUNT_PATTERN.findall(message)

    # normalize phone numbers to digits only
    normalized_phones = {
        re.sub(r"\D", "", p) for p in phones
    }

    # exclude numbers that match phone numbers
    filtered_accounts = [
        acc for acc in accounts
        if acc not in normalized_phones
    ]

    intel["bankAccounts"].extend(filtered_accounts)



    # --- Suspicious Keywords ---
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in text:
            intel["suspiciousKeywords"].append(keyword)

    # Deduplicate everything
    for key in intel:
        intel[key] = list(set(intel[key]))

    return intel
