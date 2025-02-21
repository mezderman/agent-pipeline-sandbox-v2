from core.agent import Agent
from tasks.refund_complete_node import RefundCompleteNode


class RefundCompleteAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_task(RefundCompleteNode("refund-complete-node"))
