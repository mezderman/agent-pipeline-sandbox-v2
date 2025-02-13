from dotenv import load_dotenv
import json
from core.pipeline_manager import PipelineManager
from config.enum import PipelineName
from pipelines.router_pipeline import RouterPipeline
from pipelines.refund_pipeline import RefundPipeline
from pipelines.other_pipeline import OtherPipeline
from config.pipelines_mapping import INTENT_TO_PIPELINE_MAP  # Import the mapping

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
pipeline_manager = PipelineManager.get_instance(pipeline_mapping=INTENT_TO_PIPELINE_MAP)
message_data = load_message()

# Create pipelines
other_pipeline = OtherPipeline(PipelineName.OTHER)
refund_pipeline = RefundPipeline(PipelineName.REFUND)
router_pipeline = RouterPipeline(PipelineName.ROUTER)

# Register pipelines    
pipeline_manager.register_pipeline(router_pipeline)
pipeline_manager.register_pipeline(refund_pipeline)
pipeline_manager.register_pipeline(other_pipeline)  

# Run the pipeline
final_result = pipeline_manager.run_pipeline("query-router-pipeline", message_data)

print("\nFinal Result:\n", final_result)

# After running the pipeline
logs = pipeline_manager.get_pipelines_data_logger_json()

print("\nPipeline Execution Logs:")
print(logs)

pipeline_manager.get_detailed_pipeline_map()
