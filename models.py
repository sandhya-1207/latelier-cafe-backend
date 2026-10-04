from sqlalchemy import Column, String, Float, Integer, Boolean, Text, DateTime
from datetime import datetime
from database import Base

class MenuItemModel(Base):
    __tablename__ = "menu_items"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True)
    description = Column(Text, default="")
    price = Column(Float, nullable=False)
    image = Column(String, default="")
    dietary = Column(Text, default="[]")  # JSON string
    featured = Column(Boolean, default=False)
    available = Column(Boolean, default=True)
    options = Column(Text, default="{}")  # JSON string

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    email = Column(String, default="")
    phone = Column(String, nullable=False)
    order_type = Column(String, default="pickup")
    pickup_time = Column(String, default="ASAP")
    delivery_address = Column(String, nullable=True)
    table_number = Column(String, nullable=True)
    subtotal = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    tip = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    payment_method = Column(String, default="card")
    status = Column(String, default="Received")  # Received, Preparing, Ready, Completed
    items_json = Column(Text, default="[]")
    created_at = Column(DateTime, default=datetime.utcnow)

class ReservationModel(Base):
    __tablename__ = "reservations"

    id = Column(String, primary_key=True, index=True)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)
    guests = Column(Integer, default=2)
    seating_area = Column(String, default="Sunlit Window Nook")
    occasion = Column(String, default="Casual")
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    special_requests = Column(Text, nullable=True)
    status = Column(String, default="Confirmed")
    created_at = Column(DateTime, default=datetime.utcnow)

class ReviewModel(Base):
    __tablename__ = "reviews"

    id = Column(String, primary_key=True, index=True)
    author = Column(String, nullable=False)
    role = Column(String, default="Guest")
    rating = Column(Integer, default=5)
    comment = Column(Text, nullable=False)
    date = Column(String, default="")
    avatar = Column(String, nullable=True)
    verified = Column(Boolean, default=True)
    tag = Column(String, default="General")

class ContactMessageModel(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    subject = Column(String, default="General")
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class SettingModel(Base):
    __tablename__ = "settings"

    key = Column(String, primary_key=True, index=True)
    value = Column(Text, nullable=False)

class AnalyticsModel(Base):
    __tablename__ = "analytics"

    event_name = Column(String, primary_key=True, index=True)
    count = Column(Integer, default=0)
