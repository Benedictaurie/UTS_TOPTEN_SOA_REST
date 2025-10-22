# entity_service/rental_packages.py
class RentalPackage:
    def __init__(self, rental_packages_id, type, brand, model, plate_number, 
                 description, price_per_day, is_available, created_at):
        self.id = rental_packages_id
        self.type = type
        self.brand = brand
        self.model = model
        self.plate_number = plate_number
        self.description = description
        self.price_per_day = float(price_per_day) if price_per_day else 0.0
        self.is_available = is_available
        self.created_at = created_at
    
    def to_dict(self):
        return {
            "rental_packages_id": self.id,
            "type": self.type,
            "brand": self.brand,
            "model": self.model,
            "plate_number": self.plate_number,
            "description": self.description,
            "price_per_day": self.price_per_day,
            "is_available": self.is_available,
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<RentalPackage {self.id}: {self.name}>"