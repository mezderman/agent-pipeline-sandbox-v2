from core.node import Node
from openai import OpenAI
from config.enum import EventType
class ValidateRefundNode(Node):
    def __init__(self, name):
        self.name = name
        self.client = OpenAI()

    def process(self, data):
        print("Validating refund request...")
        super().process(data)
        data = {
            **self.get_input_data(),  # Spread existing input data
            "status": "pending",
            "decision": "refund_not_eligible",
            "event": EventType.REFUND_FAIL
        }
    
        return data
