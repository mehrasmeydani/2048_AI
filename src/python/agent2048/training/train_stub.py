from __future__ import annotations

import argparse
from pathlib import Path


def run_training(config_path: str) -> int:
    config = Path(config_path)
    if not config.exists():
        print(f"Config not found: {config}")
        return 1

    print(f"[train] using config: {config}")
    print("[train] TODO: implement DQN/PPO pipeline")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Training entrypoint stub")
    parser.add_argument("--config", default="configs/train.yaml")
    args = parser.parse_args()
    return run_training(args.config)
