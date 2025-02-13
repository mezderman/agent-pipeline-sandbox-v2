import json
from config.enum import IntentType, PipelineName
from config.pipelines_mapping import INTENT_TO_PIPELINE_MAP

class PipelineManager:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PipelineManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, pipeline_mapping=None):
        if not hasattr(self, 'initialized'):
            self.pipelines = {}
            self.initialized = True
            self.pipelines_path = []
            self.pipeline_mapping = pipeline_mapping

    @classmethod
    def get_instance(cls, pipeline_mapping=None):
        if cls._instance is None:
            cls._instance = cls(pipeline_mapping=pipeline_mapping)
        return cls._instance

    def register_pipeline(self, pipeline):
        """
        Register a pipeline using its name as the key
        """
        self.pipelines[pipeline.get_name()] = pipeline
        return self.pipelines

    def get_pipeline(self, name):
        """Get a pipeline by name"""
        return self.pipelines.get(name)
    
    def run_pipeline(self, name, data):
        """Executes a specified pipeline."""
        pipeline = self.pipelines.get(name)
        if pipeline:
            self.save_pipelines_path(pipeline)
            results = pipeline.run(data)
            # Check if results is a dict and has 'intent' key
            print(f"Results: {results}")
            if hasattr(results, 'intent'):
                pipeline_name = self.pipeline_mapping[results.intent]
                results = self.run_pipeline(pipeline_name, results)
            return results
        else:
            raise ValueError(f"Pipeline {name} not found")
        
    def save_pipelines_path(self, pipeline):
        self.pipelines_path.append(pipeline)
        return self.pipelines_path
    
    def get_pipelines_path(self):
        return self.pipelines_path
    
    
    
    def get_pipelines_data_logger(self):
        pipeline_logs = []
        
        for pipeline in self.pipelines_path:
            pipeline_data = {
                "pipeline_name": pipeline.get_name(),
                "nodes_data": []
            }
            
            for node in pipeline.nodes:
                node_output = node.get_output_data() if hasattr(node, 'get_output_data') else None
                if node_output:  # Only add nodes that have data
                    node_data = {
                        "node_name": node.get_name(),
                        "output_data": node_output
                    }
                    pipeline_data["nodes_data"].append(node_data)
            
            if pipeline_data["nodes_data"]:  # Only add pipelines that have nodes with data
                pipeline_logs.append(pipeline_data)
        
        return pipeline_logs
    
    def get_pipelines_data_logger_json(self):
        logs = self.get_pipelines_data_logger()
        formatted_logs = json.dumps(logs, indent=2, cls=self.CustomJSONEncoder)
        return formatted_logs
    
    class CustomJSONEncoder(json.JSONEncoder):
        def default(self, obj):
            # Handle specific custom objects
            if hasattr(obj, '__dict__'):
                return obj.__dict__
            # Add more custom object handling if needed
            try:
                # Try to convert the object to a dict
                return vars(obj)
            except:
                # If all else fails, try string representation
                return str(obj)
    
    # def get_detailed_pipeline_map(self) -> None:
    #     """
    #     Generate and print a detailed visual representation of all pipeline connections and nodes
    #     """
    #     def add_indent_line(level: int) -> str:
    #         return "    │" + "    │" * level

    #     def add_branch_line(level: int) -> str:
    #         return "    ├────" + "    " * level

    #     def add_last_branch_line(level: int) -> str:
    #         return "    └────" + "    " * level

    #     # Header
    #     print("\n🗺️  Complete Pipeline Map")
    #     print("=" * 50)

    #     # Start with query router pipeline as it's the entry point
    #     entry_pipeline = self.pipelines.get("query-router-pipeline")
    #     if not entry_pipeline:
    #         print("\n❌ No query router pipeline found!")
    #         return

        # def process_pipeline(pipeline_name: str, visited: set, level: int = 0):
        #     if pipeline_name in visited:
        #         print(f"{add_branch_line(level)}↩️ Back to {pipeline_name}")
        #         return
            
        #     visited.add(pipeline_name)
        #     pipeline = self.pipelines.get(pipeline_name)
            
        #     if not pipeline:
        #         print(f"{add_branch_line(level)}❌ Pipeline {pipeline_name} not found!")
        #         return

        #     # Print pipeline name
        #     print(f"\n{'    ' * level}📎 Pipeline: {pipeline_name}")
            
        #     # Print nodes
        #     for i, node in enumerate(pipeline.nodes):
        #         is_last_node = i == len(pipeline.nodes) - 1
        #         prefix = add_last_branch_line(level) if is_last_node else add_branch_line(level)
                
        #         print(f"{prefix}📍 Node: {node.name}")
                
        #         # If it's a router node, show and process next pipelines
        #         if hasattr(node, 'run_next_pipeline'):
        #             print(f"{add_indent_line(level)}    Routes based on intent:")
                    
        #             # Get the routing map from the node's module
        #             routing_map = INTENT_TO_PIPELINE_MAP
                    
        #             for intent, next_pipeline in routing_map.items():
        #                 print(f"{add_indent_line(level)}    ├── If {intent.value}")
        #                 print(f"{add_indent_line(level)}    │   └──➤ {next_pipeline.value}")
                        
        #                 # Recursively process connected pipelines
        #                 if next_pipeline.value not in visited:
        #                     process_pipeline(next_pipeline.value, visited, level + 1)

        # # Start processing from the entry pipeline
        # process_pipeline("query-router-pipeline", set())

    # def print_help(self):
    #     """
    #     Print help information about pipelines and their connections
    #     """
    #     print("\n🔍 Pipeline System Help")
    #     print("=" * 50)
    #     print("\nAvailable Commands:")
    #     print("  • help    - Show this help message")
    #     print("  • list    - List all registered pipelines")
    #     print("  • run     - Run a pipeline with input data")
    #     print("\nSystem Structure:")
    #     self.get_detailed_pipeline_map()

