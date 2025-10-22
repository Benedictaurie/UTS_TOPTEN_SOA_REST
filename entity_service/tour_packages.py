# entity_service/tour_packages.py
class TourPackage:
    def __init__(self, tour_packages_id, name, description, price, duration_days, is_available, created_at):
        self.id = tour_packages_id
        self.name = name
        self.description = description
        self.price = float(price) if price else 0.0
        self.duration_days = duration_days
        self.is_available = is_available
        self.created_at = created_at

    def to_dict(self):
        return {
            "tour_packages_id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "duration_days": self.duration_days,
            "is_available": self.is_available,
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<TourPackage {self.id}: {self.name}>"
