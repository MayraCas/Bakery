
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional


class PriceSizeSchema(BaseModel):
    small: Decimal = Field(..., ge=0, decimal_places=2, description="Precio tamaño pequeño")
    medium: Decimal = Field(..., ge=0, decimal_places=2, description="Precio tamaño mediano")
    big: Decimal = Field(..., ge=0, decimal_places=2, description="Precio tamaño grande")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "small": "250.00",
                "medium": "380.00",
                "big": "500.00"
            }
        }
    )


class PriceAmountSchema(BaseModel):

    retail_sale: Decimal = Field(..., ge=0, decimal_places=2, description="Precio al por menor")
    wholesale: Decimal = Field(..., ge=0, decimal_places=2, description="Precio al por mayor")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "retail_sale": "5.00",
                "wholesale": "3.50"
            }
        }
    )


class StatusSizeSchema(BaseModel):

    small: bool = Field(True, description="Disponibilidad tamaño pequeño")
    medium: bool = Field(True, description="Disponibilidad tamaño mediano")
    big: bool = Field(True, description="Disponibilidad tamaño grande")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "small": True,
                "medium": True,
                "big": False
            }
        }
    )

