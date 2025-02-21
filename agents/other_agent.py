from core.agent import Agent
from tasks.other_node import OtherNode

class OtherAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_task(OtherNode("other-node"))
