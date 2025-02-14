from core.node import Node
from openai import OpenAI

class HumanInLoopNode(Node):
    def __init__(self, name):
        self.name = name
        self.client = OpenAI()

    def process(self, data):
        print("human in loop request...")
        
        # Create result with human in loop status
        result_data = {
            **data,  # Spread input data
            "status": "human_in_loop"
        }
        return result_data
