"""
Runnable demo of the ReasoningEngine you provided, with a minimal State
implementation, simple transform/decompose actions, and a make_dna_like_model().
"""

from collections import deque
from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple
import math
import numpy as np


@dataclass
class Action:
    name: str
    apply: Callable


@dataclass
class ReasoningResult:
    success: bool
    actions: List[str]
    final_state: Optional[object]
    explored_states: int
    explanation: str


class State:
    def __init__(self, coordinates: np.ndarray, bonds: List[Tuple[int, int]]):
        self.coordinates = coordinates.astype(float)
        self.bonds = [tuple(sorted(b)) for b in bonds]

    def clone(self):
        return State(self.coordinates.copy(), [tuple(b) for b in self.bonds])

    def __repr__(self):
        return f"State(n={len(self.coordinates)}, bonds={self.bonds})"


class ReasoningEngine:
    """Breadth-first state-transition reasoning engine with a depth limit."""

    def __init__(self, actions: List[Action], invariant: Optional[Callable] = None):
        self.actions = actions
        self.invariant = invariant or (lambda state: True)

    def state_key(self, state: State):
        coords_rounded = tuple(tuple(row) for row in np.round(state.coordinates, 6).tolist())
        bonds_sorted = tuple(sorted(tuple(int(x) for x in b) for b in state.bonds))
        return coords_rounded, bonds_sorted

    def reason(self, initial: State, goal: Callable[[State], bool], max_depth: int = 4) -> ReasoningResult:
        if not self.invariant(initial):
            return ReasoningResult(False, [], None, 0, "Initial state violates the invariants.")

        queue = deque([(initial.clone(), [])])
        visited = {self.state_key(initial)}
        explored = 0

        while queue:
            state, path = queue.popleft()
            explored += 1

            if goal(state):
                return ReasoningResult(
                    True,
                    path,
                    state,
                    explored,
                    "A valid action sequence reached the goal.",
                )

            if len(path) >= max_depth:
                continue

            for action in self.actions:
                try:
                    candidate = action.apply(state.clone())
                except (ValueError, IndexError, TypeError):
                    continue

                if not self.invariant(candidate):
                    continue

                key = self.state_key(candidate)
                if key in visited:
                    continue

                visited.add(key)
                queue.append((candidate, path + [action.name]))

        return ReasoningResult(False, [], None, explored, "No goal state found within the search depth.")


def valid_dna_state(state: State) -> bool:
    n = len(state.coordinates)
    if state.coordinates.ndim != 2 or state.coordinates.shape[1] != 3:
        return False

    for a, b in state.bonds:
        if not (0 <= a < n and 0 <= b < n):
            return False
        if a == b:
            return False

    return True


def transform(state: State, angle: float = 0.0, bend: float = 0.0) -> State:
    s = state.clone()
    cos_t = math.cos(angle)
    sin_t = math.sin(angle)
    Rz = np.array([[cos_t, -sin_t, 0.0], [sin_t, cos_t, 0.0], [0.0, 0.0, 1.0]])
    s.coordinates = s.coordinates.dot(Rz.T)
    s.coordinates[:, 1] += bend * s.coordinates[:, 0]
    return s


def decompose(state: State, bond: Tuple[int, int]) -> State:
    s = state.clone()
    a, b = tuple(sorted(bond))
    if (a, b) not in s.bonds:
        raise ValueError("Bond not present")

    s.bonds = [tuple(x) for x in s.bonds if tuple(x) != (a, b)]

    # Slightly move the fragment on one side to mimic cleavage.
    adj = {i: set() for i in range(len(s.coordinates))}
    for u, v in s.bonds:
        adj[u].add(v)
        adj[v].add(u)

    visited = {b}
    queue = deque([b])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in visited:
                visited.add(v)
                queue.append(v)

    s.coordinates[list(visited), 1] += 0.1
    return s


def make_dna_like_model() -> State:
    coords = np.array([[i * 1.0, 0.0, 0.0] for i in range(6)], dtype=float)
    bonds = [(i, i + 1) for i in range(5)]
    assert (3, 4) in bonds
    return State(coords, bonds)


actions = [
    Action("rotate_and_bend", lambda s: transform(s, angle=0.3, bend=0.02)),
    Action("cleave_bond_3_4", lambda s: decompose(s, (3, 4))),
]

engine = ReasoningEngine(actions=actions, invariant=valid_dna_state)
initial = make_dna_like_model()

result = engine.reason(
    initial=initial,
    goal=lambda s: (3, 4) not in s.bonds,
    max_depth=4,
)

print("Success:", result.success)
print("Reasoning path:", result.actions)
print("States explored:", result.explored_states)
print("Explanation:", result.explanation)
print("Final state:", result.final_state)
