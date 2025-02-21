from core.agent import Agent
from tasks.refund_task import RefundTask
from tasks.validate_refund_task import ValidateRefundTask

class RefundAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_task(RefundTask("refund-task"))
        self.add_task(ValidateRefundTask("validate-refund-task"))