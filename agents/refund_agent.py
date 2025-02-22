from core.agent import Agent
from tasks.refund_task import RefundTask
from tasks.validate_refund_task import ValidateRefundTask
from tools.refund_policy import get_refund_policy
from tools.transaction_details import get_transaction_details

class RefundAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_task(RefundTask("refund-task", [get_refund_policy, get_transaction_details]))
        self.add_task(ValidateRefundTask("validate-refund-task"))