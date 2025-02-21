from core.agent import Agent
from nodes.human_in_loop_node import HumanInLoopNode

class HumanInLoopPipeline(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_task(HumanInLoopNode("human-in-loop-node"))
