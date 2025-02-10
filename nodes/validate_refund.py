from core.node import Node
from core.memory import Memory
from openai import OpenAI

class ValidateRefundNode(Node):
    def __init__(self, name):
        self.name = name
        self.memory = Memory()
        self.client = OpenAI()

    def process(self, data):
        print("Validating refund request...")
        super().process(data)
        output_data = {
            **self.get_input_data(),  # Spread existing input data
            "status": "completed",
            "validate": "pass"
        }
    
        self.set_output_data(output_data)
        return self.get_output_data()
