from typing import List, Optional

from pydantic import BaseModel, Field


class InvoiceLineItem(BaseModel):
    description: str = Field(..., description="Line item description")
    quantity: float = Field(..., ge=0)
    unit_price: float = Field(..., ge=0)
    line_total: float = Field(..., ge=0)


class InvoiceData(BaseModel):
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    vendor_name: Optional[str] = None
    currency: Optional[str] = None
    line_items: List[InvoiceLineItem] = Field(default_factory=list)
    subtotal: float = Field(0, ge=0)
    tax: float = Field(0, ge=0)
    discount: float = Field(0, ge=0)
    total: float = Field(..., ge=0)
