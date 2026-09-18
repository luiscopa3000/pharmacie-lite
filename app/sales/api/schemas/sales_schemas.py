from datetime import datetime
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

PaymentMethod = Literal["CASH", "QR", "BANK_TRANSFER", "CARD"]

class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

class SaleCreateSchema(_StrictModel):
    cash_session_id: int | None = Field(default=None, gt=0)

class SaleItemCreateSchema(_StrictModel):
    presentation_id: int = Field(..., gt=0)
    quantity: Decimal = Field(..., gt=0, max_digits=18, decimal_places=4)

class SaleItemQuantitySchema(_StrictModel):
    quantity: Decimal = Field(..., gt=0, max_digits=18, decimal_places=4)

class PaymentSchema(_StrictModel):
    payment_method_code: PaymentMethod
    transaction_ref: str | None = Field(default=None, min_length=1, max_length=160)
    transaction_at: datetime | None = None

class SaleConfirmSchema(_StrictModel):
    payment: PaymentSchema

class SaleVoidSchema(_StrictModel):
    void_reason: str = Field(..., min_length=5, max_length=500)

class PaymentCompleteSchema(_StrictModel):
    transaction_ref: str = Field(..., min_length=1, max_length=160)
    transaction_at: datetime | None = None
    reason_text: str | None = Field(default=None, min_length=5, max_length=500)

class PaymentAuthorizeSchema(_StrictModel):
    reason_text: str = Field(..., min_length=5, max_length=500)
    valid_hours: int = Field(default=24, ge=1, le=168)
