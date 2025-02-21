from core.agent import Agent
from tasks.refund_complete_task import RefundCompleteTask


class RefundCompleteAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_task(RefundCompleteTask("refund-complete-task"))
