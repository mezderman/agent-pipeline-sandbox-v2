from core.pipeline import Pipeline
from nodes.other_node import OtherNode

class OtherPipeline(Pipeline):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_node(OtherNode("other-node"))
