import json
from database import SessionLocal, engine, Base
from cafe_models import MenuItemModel, ReviewModel, SettingModel, AnalyticsModel

Base.metadata.create_all(bind=engine)

INITIAL_SETTINGS = {
    "name": "L'Atelier Café & Botanical Roastery",
    "tagline": "Artisan Coffee, Sourdough Bakery & Slow Living",
    "heroHeadline": "Good Coffee. Great Food. Better Moments.",
    "heroSubheadline": "A sunlit sanctuary celebrating the mindful ritual of single-origin coffee, hearth-baked morning sourdough, and unhurried culinary craft in vibrant Indiranagar.",
    "heroCtaPrimary": "Explore Menu",
    "heroCtaSecondary": "Book a Table",
    "address": "123 Main Road",
    "neighborhood": "Indiranagar",
    "city": "Bengaluru, Karnataka 560038",
    "phone": "+91 9999999999",
    "email": "hello@latelier-cafe.com",
    "hoursWeekday": "Mon – Sun: 8:00 AM – 10:00 PM",
    "hoursWeekend": "Mon – Sun: 8:00 AM – 10:00 PM",
    "parkingInfo": "Dedicated valet drop-off and street parking available along 123 Main Road.",
    "transitInfo": "Walking distance from Indiranagar Metro Station (Purple Line).",
    "announcementText": "☕ Artisanal Single-Origin Coffee & Fresh Hearth Bakery • Enjoy 10% off your pickup order with code ATELIER10",
    "announcementEnabled": True,
    "instagramHandle": "@latelier-cafe1",
    "promoCode": "ATELIER10",
    "promoDiscountPercent": 10,
}

INITIAL_MENU_ITEMS = [
    {
        "id": "c-1",
        "name": "Single-Origin Pour Over (Ethiopia Yirgacheffe)",
        "category": "Coffee",
        "description": "Delicate notes of bergamot, candied peach, and jasmine blossoms. Brewed meticulously on the Chemex.",
        "price": 6.75,
        "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&q=80&w=800",
        "dietary": ["Organic", "House Specialty"],
        "featured": True,
        "available": True,
        "options": {"temperatures": ["Hot", "Iced"]}
    },
    {
        "id": "c-2",
        "name": "Velvet Flat White",
        "category": "Coffee",
        "description": "Double ristretto of our signature seasonal house espresso folded into micro-textured steamed milk.",
        "price": 5.50,
        "image": "https://images.unsplash.com/photo-1577968897966-3d4325b36b61?auto=format&fit=crop&q=80&w=800",
        "dietary": ["House Specialty"],
        "featured": True,
        "available": True,
        "options": {
            "milks": ["Whole Milk", "Oatly Barista", "House Almond", "Organic Soy"],
            "temperatures": ["Hot"],
            "extraShots": True
        }
    },
    {
        "id": "c-3",
        "name": "Cardamom Sea Salt Spanish Latte",
        "category": "Coffee",
        "description": "Rich espresso combined with condensed milk infused with freshly cracked green cardamom pods and Maldon sea salt.",
        "price": 6.50,
        "image": "https://images.unsplash.com/photo-1534778101976-62847782c213?auto=format&fit=crop&q=80&w=800",
        "dietary": ["House Specialty"],
        "featured": True,
        "available": True,
        "options": {
            "milks": ["Whole Milk", "Oatly Barista", "House Almond"],
            "temperatures": ["Hot", "Iced"],
            "sweetness": ["Less Sweet", "Regular", "Extra Sweet"],
            "extraShots": True
        }
    },
    {
        "id": "c-4",
        "name": "Artisan Cortado",
        "category": "Coffee",
        "description": "Equal parts double espresso and silky warm milk in a heavy fluted Gibraltar glass.",
        "price": 4.75,
        "image": "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&q=80&w=800",
        "dietary": ["Vegetarian"],
        "featured": False,
        "available": True,
        "options": {
            "milks": ["Whole Milk", "Oatly Barista", "House Almond"],
            "temperatures": ["Hot"],
            "extraShots": True
        }
    },
    {
        "id": "c-5",
        "name": "Yuzu Cold Brew & Tonic",
        "category": "Cold Drinks",
        "description": "20-hour steeped Kyoto cold brew layered over artisan tonic water, Japanese yuzu citrus, and fresh rosemary sprig.",
        "price": 6.95,
        "image": "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?auto=format&fit=crop&q=80&w=800",
        "dietary": ["Vegan", "Gluten-Free", "House Specialty"],
        "featured": True,
        "available": True,
        "options": {"temperatures": ["Iced"]}
    },
    {
        "id": "t-1",
        "name": "Ceremonial Uji Matcha Cloud Latte",
        "category": "Tea",
        "description": "Stone-ground ceremonial grade green tea from Kyoto whisked with vanilla bean syrup and oat cream cloud.",
        "price": 7.25,
        "image": "https://images.unsplash.com/photo-1536256263959-770b48d82b0a?auto=format&fit=crop&q=80&w=800",
        "dietary": ["Vegan", "Organic", "House Specialty"],
        "featured": True,
        "available": True,
        "options": {
            "milks": ["Oatly Barista", "House Almond", "Whole Milk"],
            "temperatures": ["Hot", "Iced"],
            "sweetness": ["Unsweetened", "Light Sweetness", "Regular"]
        }
    },
    {
        "id": "b-1",
        "name": "Avocado & Citrus Dukkah Tartine",
        "category": "Breakfast",
        "description": "Hearth-baked 36h sourdough, smashed Haas avocado, Persian feta, pickled shallots, organic microgreens, and Egyptian hazelnut dukkah.",
        "price": 14.50,
        "image": "https://images.unsplash.com/photo-1525351484163-7529414344d8?auto=format&fit=crop&q=80&w=800",
        "dietary": ["Vegetarian", "House Specialty"],
        "featured": True,
        "available": True
    },
    {
        "id": "b-2",
        "name": "Truffled Wild Mushroom Brioche",
        "category": "Breakfast",
        "description": "Sautéed chanterelles and oyster mushrooms, thyme, white truffle oil, whipped ricotta, and a 64°C slow-poached farm egg on golden brioche.",
        "price": 16.75,
        "image": "https://images.unsplash.com/photo-1509722747041-616f39b57569?auto=format&fit=crop&q=80&w=800",
        "dietary": ["Vegetarian"],
        "featured": True,
        "available": True
    },
    {
        "id": "p-1",
        "name": "Swedish Cardamom Knot (Kardemummabulle)",
        "category": "Pastries",
        "description": "Slow-fermented braided brioche rolled in butter, brown sugar, and freshly crushed Sri Lankan cardamom seeds.",
        "price": 4.85,
        "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&q=80&w=800",
        "dietary": ["Vegetarian", "House Specialty"],
        "featured": True,
        "available": True
    },
    {
        "id": "p-2",
        "name": "Sicilian Pistachio Cream Croissant",
        "category": "Pastries",
        "description": "Hand-laminated 72-layer Normandy butter croissant filled with velvet Bronte pistachio cream and dusted with crushed nuts.",
        "price": 5.75,
        "image": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&q=80&w=800",
        "dietary": ["Vegetarian", "House Specialty"],
        "featured": True,
        "available": True
    },
    {
        "id": "d-1",
        "name": "San Sebastián Basque Burnt Cheesecake",
        "category": "Desserts",
        "description": "Caramelized crust with an ultra-creamy, molten interior. Served with seasonal sour cherry reduction.",
        "price": 8.50,
        "image": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&q=80&w=800",
        "dietary": ["Vegetarian", "Gluten-Free", "House Specialty"],
        "featured": True,
        "available": True
    }
]

INITIAL_REVIEWS = [
    {
        "id": "r-1",
        "author": "Elena Rostova",
        "role": "Architect & Local",
        "rating": 5,
        "comment": "The finest espresso in Indiranagar. The natural lighting, terrazzo counters, and ambient acoustics make it my sacred morning haven.",
        "date": "September 2026",
        "verified": True,
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=200",
        "tag": "Atmosphere & Coffee"
    },
    {
        "id": "r-2",
        "author": "Marcus Chen",
        "role": "Coffee Roaster & Q-Grader",
        "rating": 5,
        "comment": "Their Ethiopia pour-over dialed on the Chemex is textbook perfection. Remarkable clarity and sparkling acidity.",
        "date": "August 2026",
        "verified": True,
        "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=200",
        "tag": "Specialty Coffee"
    }
]

def seed():
    db = SessionLocal()
    try:
        # Seed settings
        for k, v in INITIAL_SETTINGS.items():
            setting = db.query(SettingModel).filter(SettingModel.key == k).first()
            val_str = json.dumps(v) if isinstance(v, (dict, list, bool)) else str(v)
            if not setting:
                db.add(SettingModel(key=k, value=val_str))
            else:
                setting.value = val_str

        # Seed menu
        for item_data in INITIAL_MENU_ITEMS:
            existing = db.query(MenuItemModel).filter(MenuItemModel.id == item_data["id"]).first()
            if not existing:
                db.add(MenuItemModel(
                    id=item_data["id"],
                    name=item_data["name"],
                    category=item_data["category"],
                    description=item_data["description"],
                    price=item_data["price"],
                    image=item_data["image"],
                    dietary=json.dumps(item_data.get("dietary", [])),
                    featured=item_data.get("featured", False),
                    available=item_data.get("available", True),
                    options=json.dumps(item_data.get("options", {}))
                ))

        # Seed reviews
        for r_data in INITIAL_REVIEWS:
            existing_r = db.query(ReviewModel).filter(ReviewModel.id == r_data["id"]).first()
            if not existing_r:
                db.add(ReviewModel(
                    id=r_data["id"],
                    author=r_data["author"],
                    role=r_data.get("role", "Guest"),
                    rating=r_data["rating"],
                    comment=r_data["comment"],
                    date=r_data.get("date", ""),
                    avatar=r_data.get("avatar"),
                    verified=r_data.get("verified", True),
                    tag=r_data.get("tag", "General")
                ))

        # Seed analytics initial counters
        counters = [
            ("pageViews", 1420),
            ("menuViews", 980),
            ("ordersCompleted", 94),
            ("reservationsCompleted", 67),
            ("phoneClicks", 52),
            ("directionsClicks", 210)
        ]
        for name, cnt in counters:
            if not db.query(AnalyticsModel).filter(AnalyticsModel.event_name == name).first():
                db.add(AnalyticsModel(event_name=name, count=cnt))

        db.commit()
        print("Café database seeded successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
