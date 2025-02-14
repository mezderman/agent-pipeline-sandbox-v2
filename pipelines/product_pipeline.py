from core.pipeline import Pipeline
from nodes.product_node import ProductNode

class ProductPipeline(Pipeline):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_node(ProductNode("product-node")) 