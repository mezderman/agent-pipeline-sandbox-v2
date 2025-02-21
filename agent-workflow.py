from dotenv import load_dotenv
import json
from core.agent_manager import AgentManager
from config.enum import PipelineName
from pipelines.intent_router_pipeline import IntentRouterPipeline
from pipelines.refund_pipeline import RefundPipeline
from pipelines.other_pipeline import OtherPipeline
from pipelines.refund_complete_pipeline import RefundCompletePipeline
from pipelines.human_in_loop_pipeline import HumanInLoopPipeline
from config.pipelines_mapping import EVENT_TO_PIPELINE_MAP
from pipelines.product_pipeline import ProductPipeline

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
pipeline_manager = AgentManager.get_instance(pipeline_mapping=EVENT_TO_PIPELINE_MAP)
message_data = load_message()

# Create pipelines
intent_router_pipeline = IntentRouterPipeline(PipelineName.INTENT_ROUTER)
refund_pipeline = RefundPipeline(PipelineName.REFUND)
other_pipeline = OtherPipeline(PipelineName.OTHER)
refund_complete_pipeline = RefundCompletePipeline(PipelineName.REFUND_COMPLETE)
human_in_loop_pipeline = HumanInLoopPipeline(PipelineName.HUMAN_IN_LOOP)
product_pipeline = ProductPipeline(PipelineName.PRODUCT_ISSUE)

# Register pipelines    
pipeline_manager.register_agent(intent_router_pipeline)
pipeline_manager.register_agent(refund_pipeline)
pipeline_manager.register_agent(other_pipeline)  
pipeline_manager.register_agent(refund_complete_pipeline)
pipeline_manager.register_agent(human_in_loop_pipeline)
pipeline_manager.register_agent(product_pipeline)

# Run the pipeline
final_result = pipeline_manager.run_agent(PipelineName.INTENT_ROUTER, message_data)

print("\nFinal Result:\n", final_result)

# After running the pipeline
logs = pipeline_manager.get_agents_data_logger_json()

print("\nPipeline Execution Logs:")
print(logs)
