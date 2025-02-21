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
pipeline_manager = AgentManager.get_instance(agent_mapping=EVENT_TO_AGENT_MAP)
message_data = load_message()

# Create pipelines
intent_router_pipeline = IntentRouterAgent(AgentName.INTENT_ROUTER)
refund_pipeline = RefundAgent(AgentName.REFUND)
other_pipeline = OtherAgent(AgentName.OTHER)
refund_complete_pipeline = RefundCompleteAgent(AgentName.REFUND_COMPLETE)
human_in_loop_pipeline = HumanInLoopAgent(AgentName.HUMAN_IN_LOOP)
product_pipeline = ProductAgent(AgentName.PRODUCT_ISSUE)

# Register pipelines    
pipeline_manager.register_agent(intent_router_pipeline)
pipeline_manager.register_agent(refund_pipeline)
pipeline_manager.register_agent(other_pipeline)  
pipeline_manager.register_agent(refund_complete_pipeline)
pipeline_manager.register_agent(human_in_loop_pipeline)
pipeline_manager.register_agent(product_pipeline)

# Run the pipeline
final_result = pipeline_manager.run_agent(AgentName.INTENT_ROUTER, message_data)

print("\nFinal Result:\n", final_result)

# After running the pipeline
logs = pipeline_manager.get_agents_data_logger_json()

print("\nPipeline Execution Logs:")
print(logs)
