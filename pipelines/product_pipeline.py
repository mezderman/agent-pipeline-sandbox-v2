from core.agent import Agent
from nodes.product_node import ProductNode

class ProductPipeline(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_node(ProductNode("product-node")) 