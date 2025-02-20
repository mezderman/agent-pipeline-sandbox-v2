from core.agent import Agent
from nodes.other_node import OtherNode

class OtherPipeline(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_node(OtherNode("other-node"))
