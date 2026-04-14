# 2048 AI Project

Hybrid C++ and Python workspace for building a neural-network 2048 agent from baseline heuristics to trainable RL policies.

## Project Status

| Area | Status | Notes |
| --- | --- | --- |
| C++ game backend | Ready | Builds via `make build` from `src/cpp/main.cpp` |
| Python environment | Ready | In-process game logic in `src/python/agent2048/env.py` |
| Training pipeline | In progress | `train_stub.py` placeholder, DQN/PPO still to implement |
| Runtime model inference | In progress | `runtime.py` currently picks random moves |
| Tests | Started | Basic environment tests present |

## Quick Start

```bash
make build
make run
make autoplay
make train
make eval
make test
```

## Repository Structure

```text
.
|-- Makefile
|-- pyproject.toml
|-- README.md
|-- configs/
|   `-- train.yaml
|-- src/
|   |-- cpp/
|   |   `-- main.cpp
|   `-- python/
|       `-- agent2048/
|           |-- __init__.py
|           |-- env.py
|           |-- policy.py
|           |-- runtime.py
|           |-- models/
|           `-- training/
|               `-- train_stub.py
|-- scripts/
|   |-- autoplay.py
|   |-- eval.py
|   `-- train.py
|-- tests/
|   `-- test_env.py
|-- data/
|   |-- raw/
|   `-- processed/
`-- artifacts/
    |-- checkpoints/
    `-- logs/
```

## Roadmap

### Phase 1: Environment and Baselines
1. Keep a stable C++ game binary for fast deterministic gameplay.
2. Provide an in-process Python 2048 environment for RL loops.
3. Add a baseline heuristic/random policy for sanity checks.
4. Add unit tests for environment invariants and merge behavior.

### Phase 2: Data and Training Pipeline
1. Implement replay buffer and transition schema.
2. Add a DQN baseline with target network updates.
3. Save checkpoints and training metrics to `artifacts/`.
4. Add reproducible config-driven runs.

### Phase 3: Evaluation and Comparison
1. Evaluate trained models over fixed episode counts.
2. Compare average score, max score, and max tile reached.
3. Track metrics against heuristic baseline over time.

### Phase 4: Inference Integration
1. Run a trained model policy in the Python runtime loop.
2. Keep C++ game process as execution backend.
3. Support automated sweeps for benchmark runs.

## Current TODO

### Training Core
1. Replace `src/python/agent2048/training/train_stub.py` with a real trainer.
2. Implement replay buffer and transition sampling.
3. Implement a baseline DQN loop with online/target networks.
4. Save checkpoints to `artifacts/checkpoints/` and logs to `artifacts/logs/`.

### Model and Features
1. Add model code under `src/python/agent2048/models/` (MLP baseline first).
2. Add board encoding utilities (for example log2 tile encoding with empty as 0).
3. Add invalid-action masking for action selection and target computation.

### Runtime Inference
1. Replace random `choose_move` in `src/python/agent2048/runtime.py` with model inference.
2. Add model load path argument to autoplay/eval scripts.
3. Keep fallback behavior if model file is missing or invalid.

### Evaluation and Benchmarks
1. Upgrade `scripts/eval.py` to report avg/median/max score and max tile frequency.
2. Add baseline-vs-model comparison mode.
3. Add repeatable seed-based benchmark script for regressions.

### Tests and Reliability
1. Expand unit tests for merge correctness and legal action masking.
2. Add smoke test for train -> checkpoint -> eval path.
3. Add deterministic seeded tests for environment transitions.

## Learning Path and Sources

### 1) Understand this codebase first
1. Read `README.md` and `Makefile` to map command entry points.
2. Trace `scripts/train.py`, `scripts/eval.py`, and `scripts/autoplay.py`.
3. Study `src/python/agent2048/env.py` and `src/cpp/main.cpp` side by side.

Sources:
1. Python packaging tutorial: https://packaging.python.org/en/latest/tutorials/packaging-projects/
2. Makefile tutorial: https://makefiletutorial.com/
3. argparse docs: https://docs.python.org/3/library/argparse.html

### 2) Reinforcement learning foundations
1. MDP basics: state, action, reward, transition, done.
2. Why DQN works for small discrete action spaces.
3. Replay buffers, target networks, and epsilon schedules.

Sources:
1. Sutton and Barto: http://incompleteideas.net/book/the-book-2nd.html
2. OpenAI Spinning Up: https://spinningup.openai.com/en/latest/
3. DQN paper: https://www.nature.com/articles/nature14236

### 3) 2048-specific modeling choices
1. Tile encoding strategy (raw vs log2).
2. Invalid-action masking strategy.
3. Reward shaping tradeoffs for long-horizon play.

Sources:
1. Gymnasium docs: https://gymnasium.farama.org/
2. Invalid action masking paper: https://arxiv.org/abs/2006.14171

### 4) Practical implementation stack
1. Choose a model framework and keep first baseline simple.
2. Add reproducibility (seed control), checkpoints, and metrics.
3. Add benchmark reporting you can compare over commits.

Sources:
1. PyTorch tutorials: https://pytorch.org/tutorials/
2. NumPy quickstart: https://numpy.org/doc/stable/user/quickstart.html
3. Weights and Biases docs: https://docs.wandb.ai/

## Contributing

See `CONTRIBUTING.md` for local workflow, style, and pull request guidance.

## License

This project is licensed under the MIT License. See `LICENSE` for details.