from core.pipeline import Pipeline
from nodes.human_in_loop_node import HumanInLoopNode

class HumanInLoopPipeline(Pipeline):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_node(HumanInLoopNode("human-in-loop-node"))
