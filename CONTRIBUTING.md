# Contributing

## Local Workflow

1. Create or activate your virtual environment.
2. Build and verify before opening a PR.

```bash
make build
make test
make train
make eval
```

## Code Style

1. Keep changes focused and small.
2. Add tests when you change behavior.
3. Preserve project layout under src/, scripts/, configs/, tests/.
4. Keep generated outputs out of git (see .gitignore).

## Pull Request Checklist

1. Explain what changed and why.
2. Include how you validated the change.
3. Mention any follow-up work left out of scope.
4. Keep docs up to date when commands or structure change.

## Commit Guidance

1. Use clear, action-oriented commit messages.
2. Prefer one logical change per commit.
