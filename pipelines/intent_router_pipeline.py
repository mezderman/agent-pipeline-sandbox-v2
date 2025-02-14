from core.pipeline import Pipeline
from nodes.intent_router_node import IntentRouterNode

class IntentRouterPipeline(Pipeline):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_node(IntentRouterNode("intent-router-node"))
