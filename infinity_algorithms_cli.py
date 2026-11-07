"""Command-line interface for the DNA-like reasoning demonstrations."""

from __future__ import annotations

import argparse

from dna_bridge import decompose, make_dna_like_model, report, simultaneous_update, transform
from reasoning_engine import Action, ReasoningEngine, make_dna_like_model as make_linear_model, decompose as cleave_bond, transform as rotate_and_bend, valid_dna_state


def run_demo() -> int:
    """Print the DNA-like model and demonstrate transformations and cleavage."""
    original = make_dna_like_model()
    transformed = transform(original)
    decomposed = decompose(original, (3, 4))
    _, _, combined = simultaneous_update(original)

    report("Original", original)
    report("Transformation only", transformed)
    report("Decomposition only", decomposed)
    report("Simultaneous update", combined)
    return 0


def run_reasoning(max_depth: int) -> int:
    """Search for a sequence that cleaves bond (3, 4) in the linear demo model."""
    actions = [
        Action("rotate_and_bend", lambda state: rotate_and_bend(state, angle=0.3, bend=0.02)),
        Action("cleave_bond_3_4", lambda state: cleave_bond(state, (3, 4))),
    ]
    engine = ReasoningEngine(actions=actions, invariant=valid_dna_state)
    result = engine.reason(
        initial=make_linear_model(),
        goal=lambda state: (3, 4) not in state.bonds,
        max_depth=max_depth,
    )

    print(f"Success: {result.success}")
    print(f"Reasoning path: {result.actions}")
    print(f"States explored: {result.explored_states}")
    print(f"Explanation: {result.explanation}")
    print(f"Final state: {result.final_state}")
    return 0 if result.success else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="infinity-algorithms",
        description="Run the repository's DNA-like state and reasoning demonstrations.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("demo", help="show geometric and connectivity transformations")
    reason_parser = subparsers.add_parser("reason", help="search for a bond-cleavage action sequence")
    reason_parser.add_argument("--max-depth", type=int, default=4, help="maximum search depth (default: 4)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "demo":
        return run_demo()
    if args.max_depth < 0:
        raise SystemExit("--max-depth must be non-negative")
    return run_reasoning(args.max_depth)


if __name__ == "__main__":
    raise SystemExit(main())
