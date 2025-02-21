from core.agent import Agent
from tasks.other_task import OtherTask

class OtherAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_task(OtherTask("other-task"))
