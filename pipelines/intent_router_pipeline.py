from core.agent import Agent
from tasks.intent_router_node import IntentRouterNode

class IntentRouterPipeline(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_task(IntentRouterNode("intent-router-node"))
