from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class _StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

class CashOpenSchema(_StrictModel):
    opening_amount: Decimal = Field(..., ge=0, max_digits=14, decimal_places=2)

class CashOpeningAmountUpdateSchema(_StrictModel):
    opening_amount: Decimal = Field(..., ge=0, max_digits=14, decimal_places=2)

class CashCloseSchema(_StrictModel):
    counted_cash: Decimal = Field(..., ge=0, max_digits=14, decimal_places=2)
