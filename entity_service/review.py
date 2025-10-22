# entity_service/review.py
class Review:
    def __init__(self, review_id, user_id, booking_id, rating, comment, created_at):
        self.id = review_id
        self.user_id = user_id
        self.booking_id = booking_id
        self.rating = int(rating) if rating else 0
        self.comment = comment
        self.created_at =created_at

    def to_dict(self):
        return {
            "review_id": self.id,
            "user_id": self.user_id,
            "booking_id": self.booking_id,
            "rating": self.rating,
            "comment": self.comment,
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<Review {self.id} by User {self.user_id}>"