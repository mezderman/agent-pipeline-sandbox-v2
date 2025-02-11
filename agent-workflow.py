
from dotenv import load_dotenv
import json
from core.memory import Memory
from core.Pipeline import Pipeline
from nodes.query_router_node import QueryRouterNode 
from core.pipeline_manager import PipelineManager
from nodes.refund_node import RefundNode
from nodes.other_node import OtherNode
from nodes.validate_refund import ValidateRefundNode
from config.enum import PipelineName



def load_message():
    try:
        with open("data/message.json", "r") as f:
            message_data = json.load(f)
            return message_data  # Return the entire message object
    except Exception as e:
        print(f"Error loading message: {e}")
        return None
    
load_dotenv()

message_data = load_message()
memory = Memory()

# Initialize the nodes
query_router_node = QueryRouterNode("query-router-node")
refund_node = RefundNode("refund-node")
validate_refund_node = ValidateRefundNode("validate-refund-node")
other_node = OtherNode("other-node")

# Create the pipelines with names
router_pipeline = Pipeline(PipelineName.ROUTER)
refund_pipeline = Pipeline(PipelineName.REFUND)
other_pipeline = Pipeline(PipelineName.OTHER)

# Add nodes to pipelines
router_pipeline.add_node(query_router_node)
refund_pipeline.add_node(refund_node)
refund_pipeline.add_node(validate_refund_node)
other_pipeline.add_node(other_node)

# Register pipelines (now using the pipeline's name)
pipeline_manager = PipelineManager.get_instance()
pipeline_manager.register_pipeline(router_pipeline)
pipeline_manager.register_pipeline(refund_pipeline)
pipeline_manager.register_pipeline(other_pipeline)

# Run the entire pipeline sequence and get the final result
final_result = pipeline_manager.run_pipeline("query-router-pipeline", message_data)

print("\nFinal Result:\n", final_result)



# After running the pipeline
logs = pipeline_manager.get_pipelines_data_logger_json()

print("\nPipeline Execution Logs:")
print(logs)
