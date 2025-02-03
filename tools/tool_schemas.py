tools = [
    {
        "type": "function",
        "function": {
            "name": "get_refund_policy",
            "description": "Get the company's refund policy",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_transaction_details",
            "description": "Get details about a specific transaction",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Customer ID"
                    },
                    "order_id": {
                        "type": "string",
                        "description": "Order ID"
                    }
                },
                "required": ["customer_id", "order_id"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
] 