"""Grep the project's earlier Claude Code session transcripts for decision language.

Reads each JSONL line, keeps only the *text* blocks of assistant messages and of
human-typed user messages (tool results and tool inputs are skipped), splits them
into sentences, and prints sentences that contain a decision keyword, with the
session id, timestamp and role. Never prints a whole message. Output goes to the
path given as argv[2] (keep it in the scratchpad: transcripts may contain
personal text, and nothing here is copied verbatim into project outputs).

Usage: .venv/bin/python -I scripts/night/N9/grep_transcripts.py <transcript_dir> <out.tsv> [exclude_session_id ...]
"""
import json
import re
import sys
from pathlib import Path

KEYWORDS = [
    "instead of", "rather than", "decided", "decision", "we will not", "will not use",
    "do not use", "don't use", "correction", "corrected", "knock-out", "knockout",
    "negative result", "robots", "privacy", "licence", "license", "surveillance",
    "policy", "chose ", "chosen", "dropped", "rejected", "ruling", "block level",
    "block-level", "out of scope", "not claim", "cannot claim", "overstat", "inflated",
    "we decline", "declin", "deliberately", "on purpose", "trade-off", "tradeoff",
    "caveat", "lower bound", "artefact", "artifact of", "does not hold", "did not hold",
    "falsif", "disconfirm", "exclude", "excluded",
]
KW_RE = re.compile("|".join(re.escape(k) for k in KEYWORDS), re.I)
SENT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(*])")


def texts(rec):
    """Yield (role, text) for text blocks only."""
    t = rec.get("type")
    msg = rec.get("message") or {}
    if t not in ("assistant", "user"):
        return
    content = msg.get("content")
    if isinstance(content, str):
        if t == "user":
            yield "user", content
        else:
            yield "assistant", content
        return
    if not isinstance(content, list):
        return
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            yield t, block.get("text", "")


def main():
    tdir = Path(sys.argv[1])
    out = Path(sys.argv[2])
    exclude = set(sys.argv[3:])
    n = 0
    with out.open("w") as fo:
        fo.write("session\ttimestamp\trole\tsentence\n")
        for f in sorted(tdir.glob("*.jsonl")):
            sid = f.stem
            if sid in exclude:
                continue
            with f.open(encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    try:
                        rec = json.loads(line)
                    except Exception:
                        continue
                    if rec.get("isSidechain"):
                        side = "side"
                    else:
                        side = "main"
                    ts = rec.get("timestamp", "")
                    for role, txt in texts(rec):
                        if not txt or txt.startswith("<"):
                            # skip system-injected blocks (command wrappers, reminders)
                            if not txt or txt.lstrip().startswith(("<system", "<command", "<local-command", "<task-notification")):
                                continue
                        for s in SENT_RE.split(txt):
                            s = " ".join(s.split())
                            if 30 <= len(s) <= 600 and KW_RE.search(s):
                                fo.write(f"{sid[:8]}\t{ts}\t{role}/{side}\t{s}\n")
                                n += 1
    print(f"{n} sentences written to {out}")


if __name__ == "__main__":
    main()
