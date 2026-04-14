from __future__ import annotations

from typing import List

from .env import Board, Game2048Env


class HeuristicPolicy:
    """Simple baseline policy used before NN training is in place."""

    def choose(self, env: Game2048Env, board: Board) -> str:
        candidates = []
        for move in ("w", "a", "s", "d"):
            next_board, reward, changed = env._simulate(move)
            if not changed:
                continue
            empties = sum(1 for row in next_board for value in row if value == 0)
            corner = max(next_board[0][0], next_board[0][-1], next_board[-1][0], next_board[-1][-1])
            score = reward + empties * 50 + corner
            candidates.append((score, move))

        if not candidates:
            return "w"

        candidates.sort(reverse=True)
        return candidates[0][1]
