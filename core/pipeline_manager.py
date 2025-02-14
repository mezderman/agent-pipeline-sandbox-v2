import json
from config.enum import IntentType, PipelineName

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
        """Register a pipeline using its name as the key"""
        self.pipelines[pipeline.get_name()] = pipeline
        return self.pipelines

    def get_pipeline(self, name):
        """Get a pipeline by name"""
        return self.pipelines.get(name)
    
    def run_pipeline(self, name, data, visited_pipelines=None):
        """Executes a specified pipeline."""
        if visited_pipelines is None:
            visited_pipelines = set()
            
        if name in visited_pipelines:
            print(f"Warning: Detected pipeline loop at {name}, stopping recursion")
            return data
            
        visited_pipelines.add(name)
        
        pipeline = self.pipelines.get(name)
        if pipeline:
            self.save_pipelines_path(pipeline)
            results = pipeline.run(data)
            print(f"Results: {results}")
            
            if hasattr(results, 'intent') or (isinstance(results, dict) and 'intent' in results):
                # Get the intent and remove it from results
                intent = results.intent if hasattr(results, 'intent') else results['intent']
                if isinstance(results, dict):
                    results.pop('intent', None)  # Remove intent from dict
                elif hasattr(results, 'intent'):
                    delattr(results, 'intent')  # Remove intent from object
                    
                if intent in self.pipeline_mapping:
                    pipeline_name = self.pipeline_mapping[intent]
                    results = self.run_pipeline(pipeline_name, results, visited_pipelines)
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
            try:
                # Try to convert the object to a dict
                return vars(obj)
            except:
                # If all else fails, try string representation
                return str(obj)

