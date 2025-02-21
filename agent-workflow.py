from dotenv import load_dotenv
import json
from core.agent_manager import AgentManager
from config.enum import AgentName
from agents.intent_router_agent import IntentRouterAgent
from agents.refund_agent import RefundAgent
from agents.other_agent import OtherAgent
from agents.refund_complete_agent import RefundCompleteAgent
from agents.product_agent import ProductAgent
from agents.human_in_loop_agent import HumanInLoopAgent
from config.agents_mapping import EVENT_TO_AGENT_MAP


def load_message():
    try:
        with open("data/message_product_issue.json", "r") as f:
            message_data = json.load(f)
            return message_data  
    except Exception as e:
        print(f"Error loading message: {e}")
        return None


load_dotenv()
# Initialize with the mapping
agent_manager = AgentManager.get_instance(agent_mapping=EVENT_TO_AGENT_MAP)
message_data = load_message()

# Create agents
intent_router_agent = IntentRouterAgent(AgentName.INTENT_ROUTER)
refund_agent = RefundAgent(AgentName.REFUND)
other_agent = OtherAgent(AgentName.OTHER)
refund_complete_agent = RefundCompleteAgent(AgentName.REFUND_COMPLETE)
human_in_loop_agent = HumanInLoopAgent(AgentName.HUMAN_IN_LOOP)
product_agent = ProductAgent(AgentName.PRODUCT_ISSUE)

# Register agents    
agent_manager.register_agent(intent_router_agent)
agent_manager.register_agent(refund_agent)
agent_manager.register_agent(other_agent)  
agent_manager.register_agent(refund_complete_agent)
agent_manager.register_agent(human_in_loop_agent)
agent_manager.register_agent(product_agent)

# Run the agent
final_result = agent_manager.run_agent(AgentName.INTENT_ROUTER, message_data)

print("\nFinal Result:\n", final_result)

# After running the agent
logs = agent_manager.get_agents_data_logger_json()

print("Agent Execution Logs:")
print(logs)
