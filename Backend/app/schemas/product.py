from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    oldPrice: Optional[float] = None
    badge: Optional[str] = None
    color: Optional[str] = None
    sizes: Optional[List[str]] = []
    colors: Optional[List[Dict[str, Any]]] = []
    images: Optional[List[str]] = []
    details: Optional[List[str]] = []
    fit: Optional[str] = None
    category: Optional[str] = None
    stock_quantity: int = 0

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
