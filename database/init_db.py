from .db_manager import DatabaseManager

def initialize_database():
    db = DatabaseManager()
    
    # Check if database is empty
    transactions = db.read_transactions()
    
    if len(transactions) == 0:
        # Data dummy
        sample_transactions = [
            {
                'date': '2026-04-01',
                'type': 'income',
                'category': 'Salary',
                'amount': 15000000,
                'description': 'Gaji'
            },
            {
                'date': '2026-04-05',
                'type': 'expense',
                'category': 'Food',
                'amount': 75000,
                'description': 'Makan'
            },
            {
                'date': '2026-04-10',
                'type': 'expense',
                'category': 'Transport',
                'amount': 70000,
                'description': 'Bensin'
            }
        ]
        
        for transaction in sample_transactions:
            db.create_transaction(transaction)

if __name__ == "__main__":
    initialize_database()