from collections.abc import Iterator, Mapping
from typing import Any, ClassVar, override

# Partial stubs - leaving out undocumented non-private functions

decode: tuple[str, ...]
encode: tuple[str, ...]

# An abstract base class for custom filters
class FilterRefBase(Mapping[str, Any]):
    filter_id: ClassVar[str]
    filter_options: ClassVar[tuple[str, ...]]
    @override
    def __hash__(self) -> int: ...
    @override
    def __len__(self) -> int: ...
    @override
    def __iter__(self) -> Iterator[str]: ...
    @override
    def __getitem__(self, item: str) -> Any: ...
