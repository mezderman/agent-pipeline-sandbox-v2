from core.node import Node
from core.memory import Memory

class OtherNode(Node):
    def __init__(self, name):
        self.name = name
        self.memory = Memory()
        
    def process(self, data):
        print("Processing other request...")
        return {
            "status": "processing",
            "type": "other",
            "data": data
        } 