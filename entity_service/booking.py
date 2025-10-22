# entity_service/booking.py
class Booking:
    def __init__(self, booking_id, booking_code, user_id, package_id, booking_type, start_date,
                 end_date, num_persons, status, total_price, created_at):
        self.id = booking_id
        self.booking_code = booking_code
        self.user_id = user_id
        self.package_id = package_id
        self.booking_type = booking_type
        self.start_date = start_date
        self.end_date = end_date
        self.num_persons = num_persons
        self.status = status
        self.total_price = float(total_price) if total_price else 0.0
        self.created_at = created_at

    def to_dict(self):
        return {
            "booking_id": self.id,
            "booking_code": self.booking_code,
            "user_id": self.user_id,
            "package_id": self.package_id,
            "booking_type": self.booking_type,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "num_persons": self.num_persons,
            "status": self.status,
            "total_price": self.total_price,
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<Booking {self.id} for User {self.user_id}>"