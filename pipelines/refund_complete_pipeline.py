from core.agent import Agent
from nodes.refund_complete_node import RefundCompleteNode


class RefundCompletePipeline(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_task(RefundCompleteNode("refund-complete-node"))
