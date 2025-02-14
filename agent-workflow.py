from dotenv import load_dotenv
import json
from core.pipeline_manager import PipelineManager
from config.enum import PipelineName
from pipelines.intent_router_pipeline import IntentRouterPipeline
from pipelines.refund_pipeline import RefundPipeline
from pipelines.other_pipeline import OtherPipeline
from pipelines.refund_complete_pipeline import RefundCompletePipeline
from pipelines.human_in_loop_pipeline import HumanInLoopPipeline
from config.pipelines_mapping import EVENT_TO_PIPELINE_MAP

def load_message():
    try:
        with open("data/message.json", "r") as f:
            message_data = json.load(f)
            return message_data  
    except Exception as e:
        print(f"Error loading message: {e}")
        return None


load_dotenv()
# Initialize with the mapping
pipeline_manager = PipelineManager.get_instance(pipeline_mapping=EVENT_TO_PIPELINE_MAP)
message_data = load_message()

# Create pipelines
intent_router_pipeline = IntentRouterPipeline(PipelineName.INTENT_ROUTER)
refund_pipeline = RefundPipeline(PipelineName.REFUND)
other_pipeline = OtherPipeline(PipelineName.OTHER)
refund_complete_pipeline = RefundCompletePipeline(PipelineName.REFUND_COMPLETE)
human_in_loop_pipeline = HumanInLoopPipeline(PipelineName.HUMAN_IN_LOOP)

# Register pipelines    
pipeline_manager.register_pipeline(intent_router_pipeline)
pipeline_manager.register_pipeline(refund_pipeline)
pipeline_manager.register_pipeline(other_pipeline)  
pipeline_manager.register_pipeline(refund_complete_pipeline)
pipeline_manager.register_pipeline(human_in_loop_pipeline)

# Run the pipeline
final_result = pipeline_manager.run_pipeline(PipelineName.INTENT_ROUTER, message_data)

print("\nFinal Result:\n", final_result)

# After running the pipeline
logs = pipeline_manager.get_pipelines_data_logger_json()

print("\nPipeline Execution Logs:")
print(logs)
