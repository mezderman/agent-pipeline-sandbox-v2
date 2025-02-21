from core.agent import Agent
from tasks.human_in_loop_node import HumanInLoopNode

class HumanInLoopAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_task(HumanInLoopNode("human-in-loop-node"))
