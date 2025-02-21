from core.agent import Agent
from tasks.intent_router_task import IntentRouterTask

class IntentRouterAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_task(IntentRouterTask("intent-router-task"))
