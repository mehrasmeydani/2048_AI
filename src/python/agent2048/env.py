from __future__ import annotations

import random
from dataclasses import dataclass
from typing import List, Tuple


Board = List[List[int]]


@dataclass
class StepResult:
    board: Board
    reward: int
    done: bool
    changed: bool


class Game2048Env:
    """In-process 2048 environment for training loops."""

    def __init__(self, size: int = 4, seed: int | None = None) -> None:
        self.size = size
        self.rng = random.Random(seed)
        self.board: Board = [[0 for _ in range(size)] for _ in range(size)]

    def reset(self) -> Board:
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self._spawn_tile()
        self._spawn_tile()
        return self.copy_board()

    def copy_board(self) -> Board:
        return [row[:] for row in self.board]

    def legal_actions(self) -> List[str]:
        actions = []
        for move in ("w", "a", "s", "d"):
            after, reward, changed = self._simulate(move)
            if changed:
                _ = reward
                actions.append(move)
        return actions

    def step(self, action: str) -> StepResult:
        next_board, reward, changed = self._simulate(action)
        if changed:
            self.board = next_board
            self._spawn_tile()
        done = self.no_moves()
        return StepResult(board=self.copy_board(), reward=reward, done=done, changed=changed)

    def no_moves(self) -> bool:
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return False
                if r < self.size - 1 and self.board[r][c] == self.board[r + 1][c]:
                    return False
                if c < self.size - 1 and self.board[r][c] == self.board[r][c + 1]:
                    return False
        return True

    def _spawn_tile(self) -> None:
        empties = [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] == 0]
        if not empties:
            return
        r, c = self.rng.choice(empties)
        self.board[r][c] = 4 if self.rng.random() < 0.1 else 2

    def _simulate(self, move: str) -> Tuple[Board, int, bool]:
        out = self.copy_board()
        total_reward = 0
        changed = False

        if move in ("a", "d"):
            for r in range(self.size):
                line = out[r][:]
                if move == "d":
                    line.reverse()
                merged, gained = self._merge_line(line)
                if move == "d":
                    merged.reverse()
                if merged != out[r]:
                    changed = True
                out[r] = merged
                total_reward += gained
            return out, total_reward, changed

        for c in range(self.size):
            line = [out[r][c] for r in range(self.size)]
            if move == "s":
                line.reverse()
            merged, gained = self._merge_line(line)
            if move == "s":
                merged.reverse()
            for r in range(self.size):
                if out[r][c] != merged[r]:
                    changed = True
                out[r][c] = merged[r]
            total_reward += gained

        return out, total_reward, changed

    def _merge_line(self, values: List[int]) -> Tuple[List[int], int]:
        tiles = [v for v in values if v != 0]
        merged: List[int] = []
        gained = 0
        i = 0
        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                combined = tiles[i] * 2
                merged.append(combined)
                gained += combined
                i += 2
            else:
                merged.append(tiles[i])
                i += 1
        merged.extend([0] * (self.size - len(merged)))
        return merged, gained
