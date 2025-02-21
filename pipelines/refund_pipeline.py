from core.agent import Agent
from nodes.refund_node import RefundNode
from nodes.validate_refund import ValidateRefundNode

class RefundPipeline(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_task(RefundNode("refund-node"))
        self.add_task(ValidateRefundNode("validate-refund-node"))