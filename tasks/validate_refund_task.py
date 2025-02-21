from core.task import Task
from openai import OpenAI
from config.enum import EventType

class ValidateRefundTask(Task):
    def __init__(self, name):
        self.name = name
        self.client = OpenAI()

    def process(self, data):
        print("Validating refund request...")
        super().process(data)
        output_data = {
            **data,  # Spread existing input data
            "status": "pending",
            "decision": "refund_not_eligible",
            "event": EventType.REFUND_FAIL
        }
    
        return output_data
