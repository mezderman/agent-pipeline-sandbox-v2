from core.agent import Agent
from tasks.human_in_loop_task import HumanInLoopTask

class HumanInLoopAgent(Agent):
    def __init__(self, name):
        super().__init__(name)
        
        self.add_task(HumanInLoopTask("human-in-loop-task"))
