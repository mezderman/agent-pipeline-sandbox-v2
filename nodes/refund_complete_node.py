from core.node import Node
from openai import OpenAI

class RefundCompleteNode(Node):
    def __init__(self, name):
        self.name = name
        self.client = OpenAI()

    def process(self, data):
        print("human in loop request...")
        super().process(data)
        data = {
            **data,  # Spread existing input data
            "status": "refund complete"
        }
    
        return data
