# entity_service/activity_package.py
class ActivityPackage:
    def __init__(self, activity_package_id, name, description, price_per_person, is_available, created_at):
        self.id = activity_package_id
        self.name = name
        self.description = description
        self.price_per_person = float(price_per_person) if price_per_person else 0.0
        self.is_available = is_available
        self.created_at = created_at

    def to_dict(self):
        return {
            "activity_package_id": self.id, 
            "name": self.name,
            "description": self.description,
            "price_per_person": self.price_per_person,
            "is_available": self.is_available,
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<ActivityPackage {self.id}: {self.name}>"