from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
import uuid
from datetime import datetime

from database import engine, get_db, Base
from cafe_models import (
    MenuItemModel, OrderModel, ReservationModel, 
    ReviewModel, ContactMessageModel, SettingModel, AnalyticsModel
)
from cafe_schemas import (
    MenuItemCreate, MenuItemResponse,
    OrderCreate, OrderResponse, OrderStatusUpdate,
    ReservationCreate, ReservationResponse, ReservationStatusUpdate,
    ReviewCreate, ReviewResponse,
    ContactCreate, ContactResponse,
    AnalyticsTrack
)
from seed_cafe import seed

# Create DB tables
Base.metadata.create_all(bind=engine)

# Auto seed default data
try:
    seed()
except Exception as e:
    print(f"Seed notice: {e}")

app = FastAPI(
    title="L'Atelier Café & Botanical Roastery API",
    description="Full-featured RESTful backend API for menu management, online ordering, reservations, patron reviews, and real-time business telemetry.",
    version="1.0.0"
)

# Enable CORS for local dev & production hosting (e.g. Netlify)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- HEALTH ---
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "cafe": "L'Atelier Café & Botanical Roastery",
        "location": "Indiranagar, Bengaluru",
        "timestamp": datetime.utcnow().isoformat()
    }

# --- MENU ITEMS ---
@app.get("/api/menu", response_model=List[MenuItemResponse])
def get_menu(db: Session = Depends(get_db)):
    items = db.query(MenuItemModel).all()
    results = []
    for item in items:
        results.append(MenuItemResponse(
            id=item.id,
            name=item.name,
            category=item.category,
            description=item.description,
            price=item.price,
            image=item.image,
            dietary=json.loads(item.dietary or "[]"),
            featured=item.featured,
            available=item.available,
            options=json.loads(item.options or "{}") if item.options else None
        ))
    return results

@app.post("/api/menu", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
def create_menu_item(item: MenuItemCreate, db: Session = Depends(get_db)):
    item_id = item.id or f"item-{uuid.uuid4().hex[:8]}"
    db_item = MenuItemModel(
        id=item_id,
        name=item.name,
        category=item.category,
        description=item.description,
        price=item.price,
        image=item.image,
        dietary=json.dumps(item.dietary),
        featured=item.featured,
        available=item.available,
        options=json.dumps(item.options or {})
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return MenuItemResponse(
        id=db_item.id,
        name=db_item.name,
        category=db_item.category,
        description=db_item.description,
        price=db_item.price,
        image=db_item.image,
        dietary=json.loads(db_item.dietary),
        featured=db_item.featured,
        available=db_item.available,
        options=json.loads(db_item.options) if db_item.options else None
    )

@app.put("/api/menu/{item_id}", response_model=MenuItemResponse)
def update_menu_item(item_id: str, item: MenuItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(MenuItemModel).filter(MenuItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    db_item.name = item.name
    db_item.category = item.category
    db_item.description = item.description
    db_item.price = item.price
    db_item.image = item.image
    db_item.dietary = json.dumps(item.dietary)
    db_item.featured = item.featured
    db_item.available = item.available
    if item.options is not None:
        db_item.options = json.dumps(item.options)
    
    db.commit()
    db.refresh(db_item)
    return MenuItemResponse(
        id=db_item.id,
        name=db_item.name,
        category=db_item.category,
        description=db_item.description,
        price=db_item.price,
        image=db_item.image,
        dietary=json.loads(db_item.dietary),
        featured=db_item.featured,
        available=db_item.available,
        options=json.loads(db_item.options) if db_item.options else None
    )

@app.delete("/api/menu/{item_id}")
def delete_menu_item(item_id: str, db: Session = Depends(get_db)):
    db_item = db.query(MenuItemModel).filter(MenuItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    db.delete(db_item)
    db.commit()
    return {"message": f"Item {item_id} deleted successfully"}

# --- ORDERS ---
@app.get("/api/orders", response_model=List[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(OrderModel).order_by(OrderModel.created_at.desc()).all()
    results = []
    for o in orders:
        results.append(OrderResponse(
            id=o.id,
            customer_name=o.customer_name,
            email=o.email,
            phone=o.phone,
            order_type=o.order_type,
            pickup_time=o.pickup_time,
            delivery_address=o.delivery_address,
            table_number=o.table_number,
            subtotal=o.subtotal,
            discount=o.discount,
            tip=o.tip,
            total=o.total,
            payment_method=o.payment_method,
            status=o.status,
            items=json.loads(o.items_json or "[]"),
            created_at=o.created_at.strftime("%I:%M %p, %b %d")
        ))
    return results

@app.post("/api/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    order_id = f"AT-{uuid.uuid4().hex[:5].upper()}"
    db_order = OrderModel(
        id=order_id,
        customer_name=order.customer_name,
        email=order.email or "",
        phone=order.phone,
        order_type=order.order_type,
        pickup_time=order.pickup_time,
        delivery_address=order.delivery_address,
        table_number=order.table_number,
        subtotal=order.subtotal,
        discount=order.discount,
        tip=order.tip,
        total=order.total,
        payment_method=order.payment_method,
        status="Received",
        items_json=json.dumps(order.items),
        created_at=datetime.utcnow()
    )
    db.add(db_order)
    
    # Increment ordersCompleted telemetry
    stat = db.query(AnalyticsModel).filter(AnalyticsModel.event_name == "ordersCompleted").first()
    if stat:
        stat.count += 1
    else:
        db.add(AnalyticsModel(event_name="ordersCompleted", count=1))

    db.commit()
    db.refresh(db_order)

    return OrderResponse(
        id=db_order.id,
        customer_name=db_order.customer_name,
        email=db_order.email,
        phone=db_order.phone,
        order_type=db_order.order_type,
        pickup_time=db_order.pickup_time,
        delivery_address=db_order.delivery_address,
        table_number=db_order.table_number,
        subtotal=db_order.subtotal,
        discount=db_order.discount,
        tip=db_order.tip,
        total=db_order.total,
        payment_method=db_order.payment_method,
        status=db_order.status,
        items=json.loads(db_order.items_json),
        created_at=db_order.created_at.strftime("%I:%M %p")
    )

@app.patch("/api/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: str, update: OrderStatusUpdate, db: Session = Depends(get_db)):
    db_order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db_order.status = update.status
    db.commit()
    db.refresh(db_order)
    return OrderResponse(
        id=db_order.id,
        customer_name=db_order.customer_name,
        email=db_order.email,
        phone=db_order.phone,
        order_type=db_order.order_type,
        pickup_time=db_order.pickup_time,
        delivery_address=db_order.delivery_address,
        table_number=db_order.table_number,
        subtotal=db_order.subtotal,
        discount=db_order.discount,
        tip=db_order.tip,
        total=db_order.total,
        payment_method=db_order.payment_method,
        status=db_order.status,
        items=json.loads(db_order.items_json),
        created_at=db_order.created_at.strftime("%I:%M %p")
    )

# --- RESERVATIONS ---
@app.get("/api/reservations", response_model=List[ReservationResponse])
def get_reservations(db: Session = Depends(get_db)):
    res_list = db.query(ReservationModel).order_by(ReservationModel.created_at.desc()).all()
    results = []
    for r in res_list:
        results.append(ReservationResponse(
            id=r.id,
            date=r.date,
            time=r.time,
            guests=r.guests,
            seating_area=r.seating_area,
            occasion=r.occasion,
            name=r.name,
            email=r.email,
            phone=r.phone,
            special_requests=r.special_requests,
            status=r.status,
            created_at=r.created_at.strftime("%I:%M %p, %b %d")
        ))
    return results

@app.post("/api/reservations", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(res: ReservationCreate, db: Session = Depends(get_db)):
    res_id = f"RES-{uuid.uuid4().hex[:5].upper()}"
    db_res = ReservationModel(
        id=res_id,
        date=res.date,
        time=res.time,
        guests=res.guests,
        seating_area=res.seating_area,
        occasion=res.occasion or "Casual",
        name=res.name,
        email=res.email,
        phone=res.phone,
        special_requests=res.special_requests or "",
        status="Confirmed",
        created_at=datetime.utcnow()
    )
    db.add(db_res)

    # Increment reservationsCompleted telemetry
    stat = db.query(AnalyticsModel).filter(AnalyticsModel.event_name == "reservationsCompleted").first()
    if stat:
        stat.count += 1
    else:
        db.add(AnalyticsModel(event_name="reservationsCompleted", count=1))

    db.commit()
    db.refresh(db_res)

    return ReservationResponse(
        id=db_res.id,
        date=db_res.date,
        time=db_res.time,
        guests=db_res.guests,
        seating_area=db_res.seating_area,
        occasion=db_res.occasion,
        name=db_res.name,
        email=db_res.email,
        phone=db_res.phone,
        special_requests=db_res.special_requests,
        status=db_res.status,
        created_at=db_res.created_at.strftime("%I:%M %p")
    )

# --- REVIEWS ---
@app.get("/api/reviews", response_model=List[ReviewResponse])
def get_reviews(db: Session = Depends(get_db)):
    revs = db.query(ReviewModel).all()
    return [
        ReviewResponse(
            id=r.id,
            author=r.author,
            role=r.role,
            rating=r.rating,
            comment=r.comment,
            date=r.date,
            avatar=r.avatar,
            verified=r.verified,
            tag=r.tag
        )
        for r in revs
    ]

@app.post("/api/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def add_review(rev: ReviewCreate, db: Session = Depends(get_db)):
    r_id = f"r-{uuid.uuid4().hex[:6]}"
    db_rev = ReviewModel(
        id=r_id,
        author=rev.author,
        role=rev.role or "Guest",
        rating=rev.rating,
        comment=rev.comment,
        date=rev.date or "Today",
        avatar=rev.avatar,
        verified=rev.verified,
        tag=rev.tag or "General"
    )
    db.add(db_rev)
    db.commit()
    db.refresh(db_rev)
    return ReviewResponse(
        id=db_rev.id,
        author=db_rev.author,
        role=db_rev.role,
        rating=db_rev.rating,
        comment=db_rev.comment,
        date=db_rev.date,
        avatar=db_rev.avatar,
        verified=db_rev.verified,
        tag=db_rev.tag
    )

@app.delete("/api/reviews/{review_id}")
def delete_review(review_id: str, db: Session = Depends(get_db)):
    db_rev = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not db_rev:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(db_rev)
    db.commit()
    return {"message": "Review deleted"}

# --- CONTACT MESSAGES ---
@app.post("/api/contact", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def submit_contact(msg: ContactCreate, db: Session = Depends(get_db)):
    db_msg = ContactMessageModel(
        name=msg.name,
        email=msg.email,
        subject=msg.subject,
        message=msg.message,
        created_at=datetime.utcnow()
    )
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return ContactResponse(
        id=db_msg.id,
        name=db_msg.name,
        email=db_msg.email,
        subject=db_msg.subject,
        message=db_msg.message,
        created_at=db_msg.created_at.strftime("%I:%M %p, %b %d")
    )

# --- SETTINGS ---
@app.get("/api/settings")
def get_settings(db: Session = Depends(get_db)):
    settings_records = db.query(SettingModel).all()
    result = {}
    for s in settings_records:
        try:
            result[s.key] = json.loads(s.value)
        except:
            result[s.key] = s.value
    return result

@app.put("/api/settings")
def update_settings(payload: Dict[str, Any], db: Session = Depends(get_db)):
    for k, v in payload.items():
        val_str = json.dumps(v) if isinstance(v, (dict, list, bool)) else str(v)
        record = db.query(SettingModel).filter(SettingModel.key == k).first()
        if record:
            record.value = val_str
        else:
            db.add(SettingModel(key=k, value=val_str))
    db.commit()
    return {"message": "Settings updated successfully"}

# --- ANALYTICS TELEMETRY ---
@app.get("/api/analytics")
def get_analytics(db: Session = Depends(get_db)):
    rows = db.query(AnalyticsModel).all()
    return {r.event_name: r.count for r in rows}

@app.post("/api/analytics/track")
def track_event(event: AnalyticsTrack, db: Session = Depends(get_db)):
    row = db.query(AnalyticsModel).filter(AnalyticsModel.event_name == event.event_name).first()
    if row:
        row.count += 1
    else:
        row = AnalyticsModel(event_name=event.event_name, count=1)
        db.add(row)
    db.commit()
    return {"event": event.event_name, "count": row.count}
