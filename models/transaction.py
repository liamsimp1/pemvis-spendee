class Transaction:
    def __init__(self, id=None, date="", type="", category="", amount=0.0, description=""):
        self.id = id
        self.date = date
        self.type = type
        self.category = category
        self.amount = amount
        self.description = description
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'type': self.type,
            'category': self.category,
            'amount': self.amount,
            'description': self.description
        }
    
    @staticmethod
    def from_db_row(row):
        return Transaction(
            id=row[0],
            date=row[1],
            type=row[2],
            category=row[3],
            amount=row[4],
            description=row[5] if len(row) > 5 else ""
        )