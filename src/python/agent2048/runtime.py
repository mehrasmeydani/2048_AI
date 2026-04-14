from __future__ import annotations

import argparse
import os
import random
import re
import shutil
import subprocess
from typing import List, Optional

PROMPT = "Enter a number (or 1 to quit):"
Board = List[List[int]]


def parse_board(lines: List[str]) -> Optional[Board]:
    board_lines: List[List[int]] = []
    width: Optional[int] = None
    for line in reversed(lines):
        values = [int(x) for x in re.findall(r"\d+", line)]
        if width is None:
            if len(values) >= 2:
                width = len(values)
                board_lines.append(values)
            continue
        if len(values) == width:
            board_lines.append(values)
            if len(board_lines) == width:
                return list(reversed(board_lines))
        elif board_lines:
            break
    return None


def choose_move(board: Optional[Board]) -> str:
    if board is None:
        return random.choice(["w", "a", "s", "d"])
    # Placeholder: wire model inference here.
    return random.choice(["w", "a", "s", "d"])


def run(binary: str, max_steps: int = 500) -> int:
    stdbuf_path = shutil.which("stdbuf")
    cmd = [binary] if not stdbuf_path else [stdbuf_path, "-oL", "-eL", binary]

    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    assert process.stdin is not None
    assert process.stdout is not None

    lines: List[str] = []
    steps = 0

    while True:
        line = process.stdout.readline()
        if line == "":
            break

        line = line.rstrip("\n")
        print(line)
        lines.append(line)

        if "Died points:" in line or "EOF reached points:" in line:
            break

        if line.strip() == PROMPT:
            move = choose_move(parse_board(lines))
            process.stdin.write(move + "\n")
            process.stdin.flush()
            steps += 1
            if max_steps > 0 and steps >= max_steps:
                process.stdin.write("1\n")
                process.stdin.flush()

    process.wait()
    return process.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Run 2048 binary with Python control loop.")
    parser.add_argument("--binary", default="./bin/2048_cpp")
    parser.add_argument("--max-steps", type=int, default=500)
    args = parser.parse_args()

    binary = os.path.abspath(args.binary)
    if not os.path.exists(binary):
        print(f"Binary not found: {binary}")
        return 1

    return run(binary, max_steps=args.max_steps)
