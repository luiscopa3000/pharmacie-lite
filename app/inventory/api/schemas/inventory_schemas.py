from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


AdjustmentKind = Literal["ADJUSTMENT_POSITIVE", "ADJUSTMENT_NEGATIVE"]


class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class StockEntrySchema(_StrictModel):
    presentation_id: int = Field(..., gt=0)
    quantity: Decimal = Field(..., gt=0, max_digits=18, decimal_places=4)
    reason_text: str = Field(..., min_length=3, max_length=500)
    batch_code: str | None = Field(default=None, min_length=1, max_length=80)
    expiry_date: date | None = None
    expired_entry_authorized: bool = False
    authorization_reason: str | None = Field(default=None, min_length=5, max_length=500)

    @model_validator(mode="after")
    def validate_expired_authorization(self):
        if self.expired_entry_authorized and not self.authorization_reason:
            raise ValueError("authorization_reason es obligatorio cuando expired_entry_authorized=true.")
        return self


class AdjustmentSchema(_StrictModel):
    stock_lot_id: int = Field(..., gt=0)
    quantity: Decimal = Field(..., gt=0, max_digits=18, decimal_places=4)
    adjustment_kind: AdjustmentKind
    reason_text: str = Field(..., min_length=5, max_length=500)


class DisposalSchema(_StrictModel):
    stock_lot_id: int = Field(..., gt=0)
    quantity: Decimal = Field(..., gt=0, max_digits=18, decimal_places=4)
    reason_text: str = Field(..., min_length=5, max_length=500)


class LotCreateSchema(_StrictModel):
    product_id: int = Field(..., gt=0)
    batch_code: str = Field(..., min_length=1, max_length=80)
    expiry_date: date | None = None
    expired_entry_authorized: bool = False
    authorization_reason: str | None = Field(default=None, min_length=5, max_length=500)

    @model_validator(mode="after")
    def validate_expired_authorization(self):
        if self.expired_entry_authorized and not self.authorization_reason:
            raise ValueError("authorization_reason es obligatorio cuando expired_entry_authorized=true.")
        return self
