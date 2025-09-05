from collections.abc import Iterator
from typing import Any, overload

import numpy as np
from numpy.typing import NDArray
from h5py import h5s

class Selection:
    # Shape may be None if spaceid is given.
    @overload
    def __init__(
        self,
        shape: tuple[int, ...] | None,
        spaceid: h5s.SpaceID,
    ) -> None: ...
    @overload
    def __init__(
        self,
        shape: tuple[int, ...],
        spaceid: None = None,
    ) -> None: ...

    #
    @property
    def id(self) -> h5s.SpaceID: ...
    @property
    def shape(self) -> tuple[int, ...]: ...
    @property
    def nselect(self) -> int: ...
    @property
    def mshape(self) -> tuple[int, ...]: ...
    @property
    def array_shape(self) -> tuple[int, ...]: ...
    def expand_shape(self, source_shape: tuple[int, ...]) -> tuple[int, ...]: ...
    def broadcast(self, source_shape: tuple[int, ...]) -> Iterator[h5s.SpaceID]: ...

    # TODO: not sure about return type - is it Selection?
    def __getitem__(self, args: Any) -> Any: ...

class PointSelection(Selection):
    """
    Represents a point-wise selection.  You can supply sequences of
    points to the three methods append(), prepend() and set(), or
    instantiate it with a single boolean array using from_mask().
    """
    def __init__(self, shape, spaceid=..., points=...) -> None: ...
    @classmethod
    def from_mask(cls, mask: NDArray[np.bool], spaceid=...):  # -> Self:
        """Create a point-wise selection from a NumPy boolean array"""
        ...

    def append(self, points):  # -> None:
        """Add the sequence of points to the end of the current selection"""
        ...

    def prepend(self, points):  # -> None:
        """Add the sequence of points to the beginning of the current selection"""
        ...

    def set(self, points):  # -> None:
        """Replace the current selection with the given sequence of points"""
        ...

class SimpleSelection(Selection):
    """A single "rectangular" (regular) selection composed of only slices
    and integer arguments.  Can participate in broadcasting.
    """
    @property
    def mshape(self):  # -> tuple[Any, ...]:
        """Shape of current selection"""
        ...

    @property
    def array_shape(self):  # -> tuple[Any, ...]:
        ...
    def __init__(self, shape, spaceid=..., hyperslab=...) -> None: ...
    def expand_shape(self, source_shape):  # -> tuple[Any, ...]:
        """Match the dimensions of an array to be broadcast to the selection

        The returned shape describes an array of the same size as the input
        shape, but its dimensions

        E.g. with a dataset shape (10, 5, 4, 2), writing like this::

            ds[..., 0] = np.ones((5, 4))

        The source shape (5, 4) will expand to (1, 5, 4, 1).
        Then the broadcast method below repeats that chunk 10
        times to write to an effective shape of (10, 5, 4, 1).
        """
        ...

    def broadcast(self, source_shape):  # -> Generator[Any, Any, None]:
        """Return an iterator over target dataspaces for broadcasting.

        Follows the standard NumPy broadcasting rules against the current
        selection shape (self.mshape).
        """
        ...

class FancySelection(Selection):
    """
    Implements advanced NumPy-style selection operations in addition to
    the standard slice-and-int behavior.

    Indexing arguments may be ints, slices, lists of indices, or
    per-axis (1D) boolean arrays.

    Broadcasting is not supported for these selections.
    """
    @property
    def mshape(self):  # -> tuple[Any, ...]:
        ...
    @property
    def array_shape(self):  # -> tuple[Any, ...]:
        ...
    def __init__(self, shape, spaceid=..., mshape=..., array_shape=...) -> None: ...
    def expand_shape(self, source_shape): ...
    def broadcast(self, source_shape):  # -> Generator[Any, Any, None]:
        ...
