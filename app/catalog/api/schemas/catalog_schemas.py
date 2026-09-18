from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, Field, model_validator

RecordStatus = Literal["ACTIVE", "INACTIVE"]
ProductKind = Literal["MEDICINE", "OTHER_PRODUCT"]
ReferenceKind = Literal["MANUFACTURER", "DOSAGE_FORM", "ACTIVE_INGREDIENT"]


class ActiveIngredientInput(BaseModel):
    active_ingredient_id: int | None = Field(default=None, gt=0)
    name: str | None = Field(default=None, min_length=1, max_length=160)
    strength_value: Decimal | None = Field(default=None, gt=0, max_digits=18, decimal_places=6)
    strength_unit: str | None = Field(default=None, min_length=1, max_length=30)

    @model_validator(mode="after")
    def validate_reference(self):
        if self.active_ingredient_id is None and not self.name:
            raise ValueError("Debe indicar active_ingredient_id o name.")
        return self


class PresentationCreateSchema(BaseModel):
    presentation_name: str = Field(..., min_length=1, max_length=140)
    sale_unit_code: str = Field(..., min_length=1, max_length=20)
    base_units_per_presentation: Decimal = Field(..., gt=0, max_digits=18, decimal_places=4)
    sale_increment: Decimal = Field(default=Decimal("1"), gt=0, max_digits=18, decimal_places=4)
    sale_price: Decimal = Field(default=Decimal("0"), ge=0, max_digits=14, decimal_places=4)
    barcode: str | None = Field(default=None, min_length=1, max_length=64)
    is_base_presentation: bool = False
    record_status: RecordStatus = "ACTIVE"


class PresentationUpdateSchema(BaseModel):
    presentation_name: str | None = Field(default=None, min_length=1, max_length=140)
    sale_unit_code: str | None = Field(default=None, min_length=1, max_length=20)
    base_units_per_presentation: Decimal | None = Field(default=None, gt=0, max_digits=18, decimal_places=4)
    sale_increment: Decimal | None = Field(default=None, gt=0, max_digits=18, decimal_places=4)
    sale_price: Decimal | None = Field(default=None, ge=0, max_digits=14, decimal_places=4)
    barcode: str | None = Field(default=None, max_length=64)


class ProductCreateSchema(BaseModel):
    internal_code: str = Field(..., min_length=1, max_length=50)
    product_name: str = Field(..., min_length=1, max_length=180)
    product_kind: ProductKind
    base_unit_code: str = Field(..., min_length=1, max_length=20)
    category_id: int | None = Field(default=None, gt=0)
    manufacturer_id: int | None = Field(default=None, gt=0)
    dosage_form_id: int | None = Field(default=None, gt=0)
    allows_fractional_sale: bool = False
    base_quantity_step: Decimal = Field(default=Decimal("1"), gt=0, max_digits=18, decimal_places=4)
    minimum_stock: Decimal = Field(default=Decimal("0"), ge=0, max_digits=18, decimal_places=4)
    requires_lot_control: bool = False
    requires_expiry_control: bool = False
    record_status: RecordStatus = "ACTIVE"
    active_ingredients: list[ActiveIngredientInput] = Field(default_factory=list)
    presentations: list[PresentationCreateSchema] = Field(..., min_length=1)


class ProductUpdateSchema(BaseModel):
    product_name: str | None = Field(default=None, min_length=1, max_length=180)
    category_id: int | None = Field(default=None, gt=0)
    manufacturer_id: int | None = Field(default=None, gt=0)
    dosage_form_id: int | None = Field(default=None, gt=0)
    base_unit_code: str | None = Field(default=None, min_length=1, max_length=20)
    allows_fractional_sale: bool | None = None
    base_quantity_step: Decimal | None = Field(default=None, gt=0, max_digits=18, decimal_places=4)
    minimum_stock: Decimal | None = Field(default=None, ge=0, max_digits=18, decimal_places=4)
    requires_lot_control: bool | None = None
    requires_expiry_control: bool | None = None


class StatusSchema(BaseModel):
    record_status: RecordStatus


class CategoryCreateSchema(BaseModel):
    category_name: str = Field(..., min_length=1, max_length=120)


class CategoryUpdateSchema(BaseModel):
    category_name: str = Field(..., min_length=1, max_length=120)


class ReferenceUpsertSchema(BaseModel):
    reference_kind: ReferenceKind
    name: str = Field(..., min_length=1, max_length=160)
