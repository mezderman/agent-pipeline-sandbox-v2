from core.agent import Agent
from nodes.refund_node import RefundNode
from nodes.validate_refund import ValidateRefundNode

class RefundPipeline(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_node(RefundNode("refund-node"))
        self.add_node(ValidateRefundNode("validate-refund-node"))