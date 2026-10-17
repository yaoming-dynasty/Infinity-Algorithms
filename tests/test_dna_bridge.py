import numpy as np

from dna_bridge import (
    decompose,
    make_dna_like_model,
    simultaneous_update,
    transform,
)


def test_make_dna_like_model_has_expected_structure():
    state = make_dna_like_model()

    assert state.identity == "DNA-001"
    assert state.coordinates.shape == (16, 3)
    assert len(state.bonds) == 23
    assert state.history == ["initial state"]


def test_transform_preserves_connectivity():
    original = make_dna_like_model()
    transformed = transform(original, angle=0.5, bend=0.03)

    assert original.bonds == transformed.bonds
    assert transformed.coordinates.shape == original.coordinates.shape
    assert transformed.history[-1].startswith("transformation:")


def test_decompose_removes_one_bond():
    original = make_dna_like_model()
    decomposed = decompose(original, (3, 4))

    assert len(decomposed.bonds) == len(original.bonds) - 1
    assert np.array_equal(original.coordinates, decomposed.coordinates)
    assert "removed bond" in decomposed.history[-1]


def test_simultaneous_update_keeps_expected_reduction():
    original = make_dna_like_model()
    transformed, decomposed, combined = simultaneous_update(original, cleave_bond=(3, 4))

    assert original.bonds == transformed.bonds
    assert len(decomposed.bonds) == len(original.bonds) - 1
    assert len(combined.bonds) == len(original.bonds) - 1
