from core.node import Node
from openai import OpenAI
from config.enum import EventType

class ProductNode(Node):
    def __init__(self, name):
        self.name = name
        self.client = OpenAI()

    def process(self, data):
        print("Processing product request...")
        super().process(data)
        
        # Convert Pydantic model to dict if necessary
        input_data = data.model_dump() if hasattr(data, 'model_dump') else data
        
        result_data = {
            **input_data,  # Spread existing input data
            "status": "processed",
            "product_processed": True,
        }
        
        return result_data 