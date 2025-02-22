from core.agent import Agent
from tasks.product_task import ProductTask
from tools.product_manual_rag import get_product_manual
class ProductAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_task(ProductTask("product-task", [get_product_manual])) 