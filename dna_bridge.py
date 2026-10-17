
from dataclasses import dataclass, field
from copy import deepcopy

import numpy as np


@dataclass
class DNAState:
    identity: str
    coordinates: np.ndarray
    bonds: set[tuple[int, int]]
    history: list[str] = field(default_factory=list)

    def clone(self):
        return deepcopy(self)

    def components(self):
        """Connected components of the molecular graph."""
        n = len(self.coordinates)
        adjacency = [set() for _ in range(n)]

        for a, b in self.bonds:
            adjacency[a].add(b)
            adjacency[b].add(a)

        unseen = set(range(n))
        result = []

        while unseen:
            root = unseen.pop()
            component = {root}
            stack = [root]

            while stack:
                current = stack.pop()
                for neighbor in adjacency[current]:
                    if neighbor in unseen:
                        unseen.remove(neighbor)
                        component.add(neighbor)
                        stack.append(neighbor)

            result.append(sorted(component))

        return result


def make_dna_like_model():
    """
    Build a simplified two-strand helical scaffold.
    Nodes are abstract structural sites, not individual atoms.
    """
    coordinates = []
    bonds = set()

    sites_per_strand = 8
    radius = 1.0
    rise = 0.34

    for strand in range(2):
        phase = strand * np.pi

        for k in range(sites_per_strand):
            angle = k * np.pi / 2

            coordinates.append([
                radius * np.cos(angle + phase),
                radius * np.sin(angle + phase),
                rise * k
            ])

    # Backbone edges for each strand.
    for strand in range(2):
        offset = strand * sites_per_strand

        for k in range(sites_per_strand - 1):
            bonds.add((offset + k, offset + k + 1))

    # Pair corresponding sites between strands.
    for k in range(sites_per_strand):
        bonds.add((k, sites_per_strand + k))

    return DNAState(
        identity="DNA-001",
        coordinates=np.array(coordinates, dtype=float),
        bonds=bonds,
        history=["initial state"]
    )


def transform(state, angle=0.3, bend=0.02):
    """
    Geometric transformation only:
    rotate around z and bend along z.
    Does not change connectivity.
    """
    result = state.clone()

    c, s = np.cos(angle), np.sin(angle)
    rotation = np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ])

    xyz = result.coordinates
    rotated = xyz @ rotation.T

    # Illustrative bend: x displacement depends on z.
    rotated[:, 0] += bend * rotated[:, 2] ** 2

    result.coordinates = rotated
    result.history.append(
        f"transformation: angle={angle}, bend={bend}"
    )
    return result


def decompose(state, bond):
    """
    Decomposition event:
    remove one graph edge while retaining coordinates.
    """
    result = state.clone()
    edge = tuple(sorted(bond))

    if edge not in result.bonds:
        raise ValueError(f"Bond {edge} does not exist")

    result.bonds.remove(edge)
    result.history.append(f"decomposition: removed bond {edge}")
    return result


def simultaneous_update(state, angle=0.3, bend=0.02,
                        cleave_bond=(3, 4)):
    """
    Apply geometric transformation and bond cleavage
    to the same starting state.

    Both outputs derive from the same pre-update state.
    """
    transformed = transform(state, angle=angle, bend=bend)
    transformed.bonds = set(state.bonds)
    transformed.history.append("joint update: geometry branch")

    decomposed = decompose(state, cleave_bond)
    decomposed.coordinates = state.coordinates.copy()
    decomposed.history.append("joint update: connectivity branch")

    # Combined state: transformed geometry + cleaved bond.
    combined = transform(state, angle=angle, bend=bend)
    combined = decompose(combined, cleave_bond)
    combined.history.append("joint transformation-decomposition")

    return transformed, decomposed, combined


def report(label, state):
    print(f"\n--- {label} ---")
    print("Identity:", state.identity)
    print("Number of sites:", len(state.coordinates))
    print("Number of bonds:", len(state.bonds))
    print("Connected components:", state.components())
    print("History:", state.history[-2:])


if __name__ == "__main__":
    original = make_dna_like_model()

    transformed = transform(original)
    decomposed = decompose(original, (3, 4))

    t_branch, d_branch, combined = simultaneous_update(original)

    report("Original", original)
    report("Transformation only", transformed)
    report("Decomposition only", decomposed)
    report("Simultaneous update", combined)

    # Basic tests.
    assert np.array_equal(original.coordinates,
                          decomposed.coordinates)
    assert original.bonds == transformed.bonds
    assert len(decomposed.bonds) == len(original.bonds) - 1
    assert len(combined.bonds) == len(original.bonds) - 1

    print("\nAll basic tests passed.")
