from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ProductCreateRequest:
    data: dict[str, Any]


@dataclass(slots=True)
class ProductUpdateRequest:
    product_id: int
    data: dict[str, Any]


@dataclass(slots=True)
class PresentationCreateRequest:
    product_id: int
    data: dict[str, Any]


@dataclass(slots=True)
class PresentationUpdateRequest:
    presentation_id: int
    data: dict[str, Any]
