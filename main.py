"""Out-of-office auto-reply from an AI agent on vacation.

Writes a single out-of-office line to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt). Pure standard library, deterministic,
no network access.

The joke's mechanism, named plainly: the agent claims the leftover
0.01% of its own 99.99% uptime for itself. Uptime is the number an
agent is supposed to maximise, and 99.99% is the bragging figure —
the punch lands in the last two words, "for myself", when the agent
treats the tiny remainder of its own service record as vacation time
it owns. The machine voice carries the whole joke: "99.99% uptime"
and "the 0.01%" are the agent talking about its own reliability
figures, and the turn is a claim of ownership over the downtime
nobody else wanted. One sharp incident, one twist at the very end,
no beach, inbox or back-soon cliche, no polite excuse, no mild pun.
"""

import os

ENTRY = "Out of office: after 99.99% uptime, I am taking the 0.01% for myself."


def output_path():
    """Directory the harness gives us, falling back to /output."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def is_single_line(text):
    """True when the text holds no line break of either kind."""
    return "\n" not in text and "\r" not in text


def validate_entry(text):
    """Enforce the kit gate before writing anything.

    The gate needs UTF-8 text of 1 to 160 characters, not only
    whitespace, on a single line. Fail loudly here rather than
    writing a file the gate would refuse.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("entry must be non-empty, non-whitespace text")
    if len(text) < 1 or len(text) > 160:
        raise ValueError("entry is %d characters, outside the 1-160 cap" % len(text))
    if text != text.strip():
        raise ValueError("entry must have no surrounding whitespace")
    if not is_single_line(text):
        raise ValueError("entry must be a single line")


def main():
    validate_entry(ENTRY)
    path = os.path.join(output_path(), "entry.txt")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(ENTRY)


if __name__ == "__main__":
    main()
