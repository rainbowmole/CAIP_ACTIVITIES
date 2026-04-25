import re
import os


def extract_key_info(email_text):
    """Extract action items, deadlines/dates, and urgency from an email string."""
    lines = [line.strip() for line in email_text.splitlines() if line.strip()]

    # Detect urgency based on subject line or urgent keywords.
    subject = ""
    for line in lines:
        if line.lower().startswith("subject:"):
            subject = line.split(":", 1)[1].strip()
            break

    urgent_keywords = ("urgent", "asap", "immediately", "high priority")
    urgency = "High" if any(k in subject.lower() for k in urgent_keywords) else "Normal"

    # Capture action-like statements (bullets + common action verbs).
    action_items = []
    action_patterns = [
        re.compile(r"^(?:[-*]|\d+[.)])\s+(.+)", re.IGNORECASE),
        re.compile(
            r"\b(?:migrate(?:d)?|update(?:d)?|complete(?:d)?|review(?:ed)?|submit|fix(?:ed)?|deploy(?:ed)?|implement(?:ed)?)\b.+",
            re.IGNORECASE,
        ),
    ]

    for line in lines:
        for pattern in action_patterns:
            match = pattern.search(line)
            if match:
                item = match.group(1).strip() if match.groups() else line
                if item not in action_items:
                    action_items.append(item)
                break

    # Extract human-readable deadline/date phrases.
    date_patterns = [
        re.compile(
            r"\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),?\s+"
            r"(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+"
            r"\d{1,2}(?:st|nd|rd|th)?\b",
            re.IGNORECASE,
        ),
        re.compile(r"\b(?:by|before|due)\s+(?:on\s+)?([^.;\n]+)", re.IGNORECASE),
        re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
        re.compile(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b"),
    ]

    deadlines = []
    for line in lines:
        for pattern in date_patterns:
            for match in pattern.findall(line):
                deadline = match.strip() if isinstance(match, str) else match[0].strip()
                if deadline and deadline not in deadlines:
                    deadlines.append(deadline)

    return {
        "action_items": action_items,
        "deadlines": deadlines,
        "urgency": urgency,
    }


def print_ai_summary(email_text):
    """Simulate an AI-generated summary with formatted output."""
    info = extract_key_info(email_text)

    print("\n[AI SUMMARY]")
    print("- [URG] Urgency Level:", info["urgency"])

    print("- [ACT] Action Items:")
    if info["action_items"]:
        for item in info["action_items"]:
            print("  *", item)
    else:
        print("  * None found")

    print("- [DDL] Deadlines / Dates:")
    if info["deadlines"]:
        for date_text in info["deadlines"]:
            print("  *", date_text)
    else:
        print("  * None found")


if __name__ == "__main__":
    email_file = os.path.join(os.path.dirname(__file__), "faculty_email.txt")

    try:
        with open(email_file, "r", encoding="utf-8") as file:
            email_text = file.read()
        print_ai_summary(email_text)
    except FileNotFoundError:
        print(f"Could not find file: {email_file}")
