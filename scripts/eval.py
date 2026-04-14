#!/usr/bin/env python3

import argparse
import os
import random
import subprocess


def run_episode(binary: str) -> int:
    moves = [random.choice(["w", "a", "s", "d"]) for _ in range(500)] + ["1"]
    payload = "\n".join(moves) + "\n"
    proc = subprocess.run([binary], input=payload, text=True, capture_output=True, check=False)

    points = 0
    for line in proc.stdout.splitlines():
        if "points:" in line:
            try:
                points = int(line.split("points:")[-1].strip())
            except ValueError:
                pass
    return points


def main() -> int:
    parser = argparse.ArgumentParser(description="Quick evaluation harness")
    parser.add_argument("--binary", default="./bin/2048_cpp")
    parser.add_argument("--episodes", type=int, default=20)
    args = parser.parse_args()

    binary = os.path.abspath(args.binary)
    if not os.path.exists(binary):
        print(f"Binary not found: {binary}")
        return 1

    scores = [run_episode(binary) for _ in range(args.episodes)]
    avg = sum(scores) / max(1, len(scores))
    print(f"episodes={len(scores)} avg={avg:.2f} max={max(scores) if scores else 0}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
