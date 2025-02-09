class PipelineManager:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PipelineManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, name=None):
        if not hasattr(self, 'initialized'):
            self.pipelines = {}
            self.name = name
            self.initialized = True
            self.pipelines_path = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
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
    
    def run_pipeline(self, name, message_data):
        """Executes a specified pipeline."""
        pipeline = self.pipelines.get(name)
        if pipeline:
            self.save_pipelines_path(pipeline)
            return pipeline.run(message_data)
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
