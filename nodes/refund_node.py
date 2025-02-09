from core.node import Node
from core.memory import Memory

class RefundNode(Node):
    def __init__(self, name):
        self.name = name
        self.memory = Memory()
        
    def process(self, data):
        print("Processing refund request...")
        self.set_input_data(data)
        self.set_output_data({
            "status": "completed",
            "type": "refund"
        })

        return self.get_output_data()