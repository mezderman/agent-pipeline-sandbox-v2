import json

def get_transaction_details(customer_id: str, order_id: str):
    """Get transaction details for a specific order"""
    try:
        with open("data/transaction_detail.json", "r") as f:
            transactions = json.load(f)
            
        # Find matching transaction
        for transaction in transactions["transactions"]:
            if transaction["order_id"] == order_id:
                return transaction
        return None
    except Exception as e:
        print(f"Error reading transaction details: {e}")
        return None 