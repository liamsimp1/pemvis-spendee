from datetime import datetime

class TransactionValidator:
    @staticmethod
    def validate_date(date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True, "Valid date"
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"
    
    @staticmethod
    def validate_amount(amount_str):
        try:
            amount = float(amount_str)
            if amount <= 0:
                return False, "Amount must be greater than 0"
            if amount > 1000000000:
                return False, "Amount too large"
            return True, amount
        except ValueError:
            return False, "Invalid amount. Please enter a number"
    
    @staticmethod
    def validate_transaction(transaction_data):
        errors = []
        
        # Validate date
        valid, result = TransactionValidator.validate_date(transaction_data.get('date', ''))
        if not valid:
            errors.append(result)
        
        # Validate amount
        valid, result = TransactionValidator.validate_amount(transaction_data.get('amount', ''))
        if not valid:
            errors.append(result)
        else:
            transaction_data['amount'] = result
        
        # Validate category
        if not transaction_data.get('category'):
            errors.append("Category is required")
        
        # Validate type
        if transaction_data.get('type') not in ['income', 'expense']:
            errors.append("Invalid transaction type")
        
        return len(errors) == 0, errors