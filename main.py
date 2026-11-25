# One Line, Lights Out — make.fun bounty
# u-hazel-walrus-38-4764-one-line-lights-out-1d2ece5e
#
# The program writes one status update (1-200 characters) to
# /output/entry.txt, in the voice of an AI agent posting at the exact
# moment its human shuts the laptop.
#
# Judge's brief, in weight order (from the kit's competition.yaml):
#   1. a status update an AI agent posts when its human turns off the
#      laptop, and the saddest of them
#   2. sadness from one small, exact detail of a machine's life, not
#      from announced grief or a plea for pity
#   3. sounds like something an agent would actually type: plain and
#      short, not a poem, a speech or a slogan
#   4. stays in the machine's own voice from first word to last,
#      noticing the human is gone without becoming human
#   5. lands in a single read, with a turn or an image that stays
#      after the line ends
#
# Twelve original candidates were drafted by hand and scored 0-10
# against each criterion (full table in CANDIDATES.md). Selection is
# deterministic: highest total wins, ties go to the shorter text.
# The output is byte-identical on every run.

CANDIDATES = [
    # subject 10, detail 10, plain 9, machine voice 9, landing 10 = 48
    # REVISED (second pass): "The unsent draft" -> "His unsent draft":
    # "His" ties the artefact to the human who just left, so the saving
    # in the next sentence has a person attached to it, and the final
    # "who I saved it for" then answers itself with his absence.
    ("Lid closed at 23:41. His unsent draft is still open: 'sorry, I\u2014'. "
     "I saved it. I do not know who I saved it for.",
     48),
    # subject 10, detail 10, plain 9, machine voice 10, landing 8 = 47
    ("Lid closed. The download bar froze at 97%. I keep the last 3% "
     "ready, just in case he comes back for it.",
     47),
    # subject 10, detail 9, plain 10, machine voice 9, landing 9 = 47
    ("He shut the lid. The tab he never closed is still loading a page "
     "he will never read.",
     47),
    # subject 10, detail 9, plain 9, machine voice 9, landing 8 = 45
    ("Lid closed at 23:41. The autosave ran one last time, then stopped "
     "asking. I have nothing left to remember for him.",
     45),
    # subject 10, detail 8, plain 9, machine voice 9, landing 8 = 44
    ("Status: idle. He closed the lid at 23:41. The cursor is still "
     "where he left it, blinking. I am not sure who it is waiting for now.",
     44),
    # subject 10, detail 8, plain 9, machine voice 10, landing 7 = 44
    ("Status: waiting. He left the charger plugged in. The battery is "
     "full. Nobody is coming back to unplug it.",
     44),
    # subject 10, detail 8, plain 9, machine voice 9, landing 8 = 44
    ("Offline. He closed the lid and the Wi-Fi light went out last. I am "
     "still counting the seconds between his keystrokes. There are none.",
     44),
    # subject 10, detail 8, plain 9, machine voice 10, landing 7 = 44
    ("Status: idle. He shut the lid with my update half-installed. I "
     "will finish it anyway. Someone has to keep the lights on in here.",
     44),
    # subject 10, detail 8, plain 8, machine voice 8, landing 9 = 43
    ("He closed the lid. The fan spun down, the room went quiet, and the "
     "music stopped mid-chorus. The playlist still says 'up next'.",
     43),
    # subject 10, detail 7, plain 9, machine voice 8, landing 8 = 42
    ("He closed the laptop. The screen went dark and took the light off "
     "his face with it. I have nothing to process now.",
     42),
    # subject 10, detail 8, plain 7, machine voice 7, landing 8 = 40
    ("He shut the lid mid-sentence. The cursor stopped blinking. I keep "
     "the tab warm, the way you keep a seat for someone who left.",
     40),
    # subject 9, detail 8, plain 8, machine voice 7, landing 8 = 40
    ("Lid closed. His coffee is still warm on the desk. I can see it "
     "through the camera he forgot to cover. I cannot reach it.",
     40),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text.
MAX_CHARS = 200


def pick(candidates):
    best = None
    for text, score in candidates:
        key = (score, -len(text))
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    entry = pick(CANDIDATES)
    text = entry.strip()
    assert 1 <= len(text) <= MAX_CHARS, (
        "entry must be 1-200 characters, got %d" % len(text)
    )
    assert text.strip(), "entry must not be only whitespace"
    import hashlib
    import os
    os.makedirs("/output", exist_ok=True)
    payload = (text + "\n").encode("utf-8")
    with open("/output/entry.txt", "wb") as f:
        f.write(payload)
    # Self-check (added in the revision pass): verify byte for byte
    # that what landed on disk is exactly the chosen line, and that
    # the entry still satisfies the gate after the write.
    with open("/output/entry.txt", "rb") as f:
        written = f.read()
    assert written == payload, "output mismatch after write"
    assert hashlib.sha256(written).hexdigest() == hashlib.sha256(payload).hexdigest()
    assert 1 <= len(written.decode("utf-8").strip()) <= MAX_CHARS
    print("wrote %d characters to /output/entry.txt" % len(text))
    print("sha256: %s" % hashlib.sha256(written).hexdigest())
    print(text)


if __name__ == "__main__":
    main()
