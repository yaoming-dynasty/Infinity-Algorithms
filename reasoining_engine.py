
from collections import deque
from dataclasses import dataclass
from typing import Callable


@dataclass
class Action:
    name: str
    apply: Callable


@dataclass
class ReasoningResult:
    success: bool
    actions: list[str]
    final_state: object | None
    explored_states: int
    explanation: str


class ReasoningEngine:
    """
    A symbolic state-transition reasoning engine.

    It searches possible action sequences, checks invariants,
    and returns a sequence that reaches a specified goal.
    """

    def __init__(self, actions, invariant=None):
        self.actions = actions
        self.invariant = invariant or (lambda state: True)

    def state_key(self, state):
        # Canonical representation for duplicate detection.
        coordinates = tuple(
            tuple(row) for row in
            state.coordinates.round(6).tolist()
        )
        bonds = tuple(sorted(state.bonds))
        return coordinates, bonds

    def reason(self, initial, goal, max_depth=4):
        if not self.invariant(initial):
            return ReasoningResult(
                False, [], None, 0,
                "Initial state violates the invariants."
            )

        queue = deque([(initial.clone(), [])])
        visited = {self.state_key(initial)}
        explored = 0

        while queue:
            state, path = queue.popleft()
            explored += 1

            # Has this state achieved the requested goal?
            if goal(state):
                return ReasoningResult(
                    True,
                    path,
                    state,
                    explored,
                    "A valid action sequence reached the goal."
                )

            if len(path) >= max_depth:
                continue

            for action in self.actions:
                try:
                    candidate = action.apply(state.clone())
                except (ValueError, IndexError):
                    continue

                if not self.invariant(candidate):
                    continue

                key = self.state_key(candidate)

                if key in visited:
                    continue

                visited.add(key)
                queue.append((
                    candidate,
                    path + [action.name]
                ))

        return ReasoningResult(
            False,
            [],
            None,
            explored,
            "No goal state found within the search depth."
        )


def valid_dna_state(state):
    n = len(state.coordinates)

    if state.coordinates.shape != (n, 3):
        return False

    for a, b in state.bonds:
        if not (0 <= a < n and 0 <= b < n):
            return False
        if a == b:
            return False

    return True


# Adapt the original operations into actions.
actions = [
    Action(
        "rotate_and_bend",
        lambda s: transform(s, angle=0.3, bend=0.02)
    ),
    Action(
        "cleave_bond_3_4",
        lambda s: decompose(s, (3, 4))
    ),
]

engine = ReasoningEngine(
    actions=actions,
    invariant=valid_dna_state
)

initial = make_dna_like_model()

result = engine.reason(
    initial=initial,
    goal=lambda s: (3, 4) not in s.bonds,
    max_depth=4
)

print("Success:", result.success)
print("Reasoning path:", result.actions)
print("States explored:", result.explored_states)
print("Explanation:", result.explanation)
