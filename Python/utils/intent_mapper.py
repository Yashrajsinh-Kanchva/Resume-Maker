ALLOWED_KEYWORDS = [
    "resume",
    "cv",
    "template",
    "download",
    "edit",
    "create",
    "make",
    "build",
    "ats",
    "score",
    "ai",
    "pricing",
    "price",
    "subscription",
    "billing",
    "payment",
    "login",
    "signin",
    "signup",
    "account",
    "profile",
    "contact",
    "support",
    "help",
    "faq",
    "cancel",
    "design",
    "document",
]

INTENTS = [
    ("contact", "GO_TO_CONTACT"),
    ("support", "GO_TO_CONTACT"),
    ("pricing", "GO_TO_PRICING"),
    ("price", "GO_TO_PRICING"),
    ("faq", "SCROLL_FAQ")
]


def is_website_question(text: str) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in ALLOWED_KEYWORDS)


def detect_intent(text: str) -> str:
    text = text.lower()
    for keyword, intent in INTENTS:
        if keyword in text:
            return intent
    return "NONE"
