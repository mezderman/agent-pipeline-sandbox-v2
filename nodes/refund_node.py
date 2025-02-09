from core.node import Node
from core.memory import Memory

class RefundNode(Node):
    def __init__(self, name):
        self.name = name
        self.memory = Memory()
        
    def process(self, data):
        print("Processing refund request...")
        return {
            "status": "processing",
            "type": "refund",
            "data": data
        } 