from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime

# Menu
class MenuItemCreate(BaseModel):
    id: Optional[str] = None
    name: str
    category: str
    description: str = ""
    price: float
    image: str = ""
    dietary: List[str] = []
    featured: bool = False
    available: bool = True
    options: Optional[Dict[str, Any]] = None

class MenuItemResponse(BaseModel):
    id: str
    name: str
    category: str
    description: str
    price: float
    image: str
    dietary: List[str]
    featured: bool
    available: bool
    options: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

# Orders
class OrderItemSchema(BaseModel):
    id: Optional[str] = None
    menu_item_id: str
    name: str
    quantity: int
    customization: Optional[Dict[str, Any]] = None
    item_total: float

class OrderCreate(BaseModel):
    customer_name: str
    email: Optional[str] = ""
    phone: str
    order_type: str = "pickup"
    pickup_time: str = "ASAP"
    delivery_address: Optional[str] = None
    table_number: Optional[str] = None
    subtotal: float
    discount: float = 0.0
    tip: float = 0.0
    total: float
    payment_method: str = "card"
    items: List[Dict[str, Any]] = []

class OrderStatusUpdate(BaseModel):
    status: str

class OrderResponse(BaseModel):
    id: str
    customer_name: str
    email: str
    phone: str
    order_type: str
    pickup_time: str
    delivery_address: Optional[str]
    table_number: Optional[str]
    subtotal: float
    discount: float
    tip: float
    total: float
    payment_method: str
    status: str
    items: List[Dict[str, Any]]
    created_at: str

# Reservations
class ReservationCreate(BaseModel):
    date: str
    time: str
    guests: int = 2
    seating_area: str = "Sunlit Window Nook"
    occasion: Optional[str] = "Casual"
    name: str
    email: str
    phone: str
    special_requests: Optional[str] = ""

class ReservationStatusUpdate(BaseModel):
    status: str

class ReservationResponse(BaseModel):
    id: str
    date: str
    time: str
    guests: int
    seating_area: str
    occasion: Optional[str]
    name: str
    email: str
    phone: str
    special_requests: Optional[str]
    status: str
    created_at: str

# Reviews
class ReviewCreate(BaseModel):
    author: str
    role: Optional[str] = "Guest"
    rating: int = 5
    comment: str
    date: Optional[str] = "Today"
    avatar: Optional[str] = None
    verified: bool = True
    tag: Optional[str] = "General"

class ReviewResponse(BaseModel):
    id: str
    author: str
    role: str
    rating: int
    comment: str
    date: str
    avatar: Optional[str]
    verified: bool
    tag: str

# Contact
class ContactCreate(BaseModel):
    name: str
    email: str
    subject: str = "General Inquiry"
    message: str

class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    subject: str
    message: str
    created_at: str

# Analytics
class AnalyticsTrack(BaseModel):
    event_name: str
