# Infinity-Algorithms

Infinity-Algorithms pairs a speculative “Dynamic Boundary Framework” with small, runnable Python experiments. The executable portion models DNA-like structures as coordinates and graph bonds, then explores geometric transforms and bond-cleavage transitions while checking simple invariants. It is an educational prototype, not a molecular simulator or a general-purpose theorem prover.

## Conceptual framework

The README's central expression is:

$$\{-0, \vert{}-0\vert{}, \vert{}0\vert{}, 0\} \implies \{INFINITY\}$$

The project treats this as a conceptual progression from a collapsed baseline, through a transition, to an expanded state. In the code, that idea is represented concretely as a state, a set of allowed actions, invariants that constrain valid states, and a goal condition. The mathematical/philosophical claims are conceptual framing; the Python demos do not prove those claims.

## Quick start

Requires Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

Run the command-line demonstrations:

```bash
infinity-algorithms reason
infinity-algorithms reason --max-depth 4
infinity-algorithms demo
```

Or run without installing the console script:

```bash
python -m infinity_algorithms_cli reason
python dna_bridge.py
```

## Development

```bash
make help
make test
make lint
make demo
```

The same test suite can be run with `python -m pytest -q`. The CI workflow runs tests, syntax compilation, and critical lint checks on pushes and pull requests.

## Project layout

- `dna_bridge.py` — a 16-site DNA-like graph, geometric transform, bond cleavage, and simultaneous update demo.
- `reasoning_engine.py` — `State`, `Action`, and a breadth-first `ReasoningEngine` with a depth limit and invariant/goal callbacks.
- `infinity_algorithms_cli.py` — CLI for the graph demo and bounded reasoning search.
- `examples/` — standalone reasoning example.
- `tests/` — tests for DNA-like operations and CLI behavior.
- `Axioms.md`, `Formalization.md`, `Set-Theory-Paradoxes.md`, and related markdown files — conceptual notes and framework documentation.

## Model limitations

The DNA structures are simplified graphs, not atomistic representations. The reasoning engine searches a finite action/state space up to a configured depth; its success means only that the supplied goal predicate was reached while the supplied invariant held. It does not establish a general conclusion about infinity, identity, or physical DNA.
