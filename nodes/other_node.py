from core.node import Node

class OtherNode(Node):
    def __init__(self, name):
        self.name = name
        
    def process(self, data):
        print("Processing other request...")
        super().process(data)
        data = {
            "status": "completed",
            "type": "other"
        }
        return data