# 2048 AI Project

This repository is structured to evolve from a heuristic 2048 controller into a full neural-network training and evaluation pipeline.

## Project Plan

### Phase 1: Environment and Baselines
1. Keep a stable C++ game binary for fast deterministic gameplay.
2. Provide an in-process Python 2048 environment for RL loops.
3. Add a baseline heuristic/random policy for sanity checks.
4. Add unit tests for environment invariants and merge behavior.

### Phase 2: Data and Training Pipeline
1. Implement replay buffer and transition schema.
2. Add a DQN baseline with target network updates.
3. Save checkpoints and training metrics to artifacts.
4. Add reproducible config-driven runs.

### Phase 3: Evaluation and Comparison
1. Evaluate trained models over fixed episode counts.
2. Compare average score, max score, and max tile reached.
3. Track metrics against heuristic baseline over time.

### Phase 4: Inference Integration
1. Run a trained model policy in the Python runtime loop.
2. Keep C++ game process as execution backend.
3. Support automated sweeps for benchmark runs.

## Repository Structure

```
.
├── Makefile
├── pyproject.toml
├── README.md
├── configs/
│   └── train.yaml
├── src/
│   ├── cpp/
│   │   └── main.cpp
│   └── python/
│       └── agent2048/
│           ├── __init__.py
│           ├── env.py
│           ├── policy.py
│           ├── runtime.py
│           ├── models/
│           └── training/
│               └── train_stub.py
├── scripts/
│   ├── autoplay.py
│   ├── eval.py
│   └── train.py
├── tests/
│   └── test_env.py
├── data/
│   ├── raw/
│   └── processed/
└── artifacts/
	├── checkpoints/
	└── logs/
```

## Build and Run

### Build C++ binary

```bash
make build
```

### Run game manually

```bash
make run
```

### Run Python controller against C++ binary

```bash
make autoplay
```

## Training and Evaluation Entry Points

### Training stub

```bash
make train
```

### Evaluation harness

```bash
make eval
```

### Unit tests

```bash
make test
```

## Notes

1. `func.py` remains as a compatibility launcher and now delegates to `agent2048.runtime`.
2. The runtime currently uses a placeholder move chooser; replace it with NN inference in `src/python/agent2048/runtime.py`.
3. `configs/train.yaml` is the configuration anchor for upcoming DQN/PPO implementation.

## Current TODO

### Training Core
1. Replace `src/python/agent2048/training/train_stub.py` with a real trainer.
2. Implement replay buffer and transition sampling.
3. Implement a baseline DQN loop (online net, target net, epsilon-greedy policy).
4. Save checkpoints to `artifacts/checkpoints/` and training logs to `artifacts/logs/`.

### Model and Features
1. Add model code under `src/python/agent2048/models/` (MLP baseline first).
2. Add board encoding utilities (for example log2 tile encoding with empty as 0).
3. Add action masking for invalid moves during action selection and target computation.

### Runtime Inference
1. Replace random `choose_move` in `src/python/agent2048/runtime.py` with model inference.
2. Add model load path argument to autoplay/eval scripts.
3. Keep fallback behavior if model file is missing or invalid.

### Evaluation and Benchmarks
1. Upgrade `scripts/eval.py` to report avg/median/max score and max tile frequency.
2. Add baseline-vs-model comparison mode.
3. Add repeatable seed-based benchmark script for regression checks.

### Tests and Reliability
1. Expand unit tests for merge correctness and legal action masking.
2. Add smoke test for train->checkpoint->eval path.
3. Add deterministic seeded tests for environment transitions.

## Research Roadmap

### 1) Understand the repo flow first
1. Read [README.md](README.md) top to bottom.
2. Open [Makefile](Makefile) to see how build, run, train, eval, and test are wired.
3. Follow the entry scripts in [scripts/train.py](scripts/train.py), [scripts/eval.py](scripts/eval.py), and [scripts/autoplay.py](scripts/autoplay.py).
4. Trace package internals in [src/python/agent2048/env.py](src/python/agent2048/env.py), [src/python/agent2048/runtime.py](src/python/agent2048/runtime.py), and [src/python/agent2048/training/train_stub.py](src/python/agent2048/training/train_stub.py).
5. Review [src/cpp/main.cpp](src/cpp/main.cpp) to understand runtime game behavior and I/O format.

Starter sources:
1. Python packaging basics: https://packaging.python.org/en/latest/tutorials/packaging-projects/
2. Makefile basics: https://makefiletutorial.com/
3. argparse (CLI design): https://docs.python.org/3/library/argparse.html

### 2) Learn RL fundamentals for this project
1. Learn MDP framing: state, action, reward, transition, done.
2. Learn value-based RL and why DQN fits small discrete action spaces.
3. Understand exploration vs exploitation and epsilon-greedy scheduling.
4. Understand replay buffers and target networks for DQN stability.

Starter sources:
1. Sutton and Barto (book): http://incompleteideas.net/book/the-book-2nd.html
2. OpenAI Spinning Up (conceptual intro): https://spinningup.openai.com/en/latest/
3. DeepMind DQN paper (original): https://www.nature.com/articles/nature14236

### 3) Learn 2048-specific representation choices
1. Research board encodings (raw tiles vs log2 encoding).
2. Research invalid-action masking for environments with illegal moves.
3. Research reward shaping tradeoffs for sparse long-horizon games.

Starter sources:
1. Gymnasium API (environment patterns): https://gymnasium.farama.org/
2. Invalid action masking discussion and patterns: https://arxiv.org/abs/2006.14171

### 4) Learn implementation tools you will likely use
1. Pick one DL framework for models and training loop integration.
2. Learn checkpointing, deterministic seeds, and experiment logging.
3. Learn basic evaluation statistics (mean, median, percentiles, confidence intervals).

Starter sources:
1. PyTorch beginner and RL docs: https://pytorch.org/tutorials/
2. NumPy quickstart: https://numpy.org/doc/stable/user/quickstart.html
3. Weights and Biases docs (optional logging): https://docs.wandb.ai/

### 5) Suggested order for first implementation pass
1. Implement replay buffer and a minimal DQN trainer in [src/python/agent2048/training/train_stub.py](src/python/agent2048/training/train_stub.py).
2. Add first MLP model file under [src/python/agent2048/models](src/python/agent2048/models).
3. Add checkpoint save/load and metrics logging to artifacts folders.
4. Replace random move selection in [src/python/agent2048/runtime.py](src/python/agent2048/runtime.py) with model inference.
5. Upgrade [scripts/eval.py](scripts/eval.py) to report stable benchmark metrics.