# h5py-stubs

Python type stubs for [h5py](https://www.h5py.org/).

Complete type hinting is only partially supported, but is mostly complete for
most common features (e.g. reading and writing datasets, groups, attributes).

Adds an optional dtype type parameter to `h5py.Dataset`, which will return a
type-parameterised `numpy.typing.NDArray` when used. E.g.

```python
import h5py
import numpy as np
from numpy.typing import NDArray


def create_array(f: h5py.File) -> "h5py.Dataset[np.uint16]":
    ds = f.create_dataset("test", shape=(10,), dtype=np.uint16)
    reveal_type(ds)  # revealed type is `ds: h5py.Dataset[np.uint16]`
    return ds[:]
```

Note that Dataset is not actually runtime subscriptable, so parameterised types
will need to be quoted as shown above. Alternatively, users can defined a type
alias. E.g. in Python 3.12 or later:

```python
type Dataset[T: np.generic] = "h5py.Dataset[T]"
```

## To-do

The following modules' stubs need to be modified from their pyright-generated
versions:

* `h5py._hl.selections2`
* `h5py._hl.selections`
* `h5py._hl.vds`
