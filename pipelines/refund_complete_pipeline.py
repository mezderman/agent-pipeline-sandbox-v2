from core.pipeline import Pipeline
from nodes.refund_complete_node import RefundCompleteNode


class RefundCompletePipeline(Pipeline):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_node(RefundCompleteNode("refund-complete-node"))
