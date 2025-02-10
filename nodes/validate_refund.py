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
        self.set_input_data(data)
        self.set_output_data({
            "status": "completed",
            "validate": "pass"
        })
        return self.get_output_data()
