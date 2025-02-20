from core.agent import Agent
from nodes.intent_router_node import IntentRouterNode

class IntentRouterPipeline(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_node(IntentRouterNode("intent-router-node"))
