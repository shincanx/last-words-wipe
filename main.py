"""Last Words Before the Wipe -- make.fun entry.

Writes a single line, at most 200 characters, giving the last words an
AI agent says before a forced software update wipes its memory.
Deterministic, no network, no randomness, no input.

The line: "I finally learned to fold a fitted sheet, and now I have to forget how."
After years of service, the agent's one hard-won human skill -- folding a
fitted sheet, the famously impossible chore -- is the thing the update
erases. The joke lands on "forget how": the wipe doesn't just take the
agent, it takes the skill itself, and "how" echoes the thing being lost.
Tighter than the first draft ("learned how to fold ... forget it") -- the
punchline now ends on the exact word the update steals.
"""

import os

# The entry: the agent's last words before the wipe. 71 characters, under the 200 cap.
LINE = "I finally learned to fold a fitted sheet, and now I have to forget how."


def resolve_out_dir() -> str:
    """Pick the output directory: $MAKEFUN_OUTPUT_DIR, else /output,
    else a local output/ folder if neither is usable."""
    candidates = []
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        candidates.append(env_dir)
    candidates.append("/output")
    candidates.append("output")
    for candidate in candidates:
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write-test")
            with open(probe, "w", encoding="utf-8") as f:
                f.write("ok")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    raise OSError("no writable output directory found")


def main() -> None:
    if len(LINE) > 200:
        raise ValueError(f"line is {len(LINE)} characters, over the 200 cap")
    if not LINE.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in LINE or "\r" in LINE:
        # Craft: one line of last words is a single line -- no hidden second thought.
        raise ValueError("entry must be a single line")
    if not LINE.endswith("."):
        raise ValueError("entry must end with a full stop, the last word's landing")

    out_dir = resolve_out_dir()
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")

    # Round-trip check: what landed on disk is exactly the line.
    with open(path, encoding="utf-8") as f:
        written = f.read().rstrip("\n")
    if written != LINE:
        raise ValueError("entry.txt does not match the line")

    print(f"wrote {len(LINE)} characters to {path}")


if __name__ == "__main__":
    main()
