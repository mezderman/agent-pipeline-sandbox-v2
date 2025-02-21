from core.agent import Agent
from tasks.product_task import ProductTask

class ProductAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_task(ProductTask("product-task")) 