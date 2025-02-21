from core.agent import Agent
from tasks.refund_node import RefundNode
from tasks.validate_refund import ValidateRefundNode

class RefundAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_task(RefundNode("refund-node"))
        self.add_task(ValidateRefundNode("validate-refund-node"))