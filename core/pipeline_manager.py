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

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register_pipeline(self, pipeline, name=None):
        """Register a pipeline with the manager
        Args:
            pipeline: Pipeline instance to register
            name: Optional name for the pipeline. If not provided, uses self.name
        """
        pipeline_name = name if name else self.name
        self.pipelines[pipeline_name] = pipeline

    def get_pipeline(self, name):
        """Get a pipeline by name"""
        return self.pipelines.get(name)
    
    def run_pipeline(self, name, message_data):
        """Executes a specified pipeline."""
        pipeline = self.pipelines.get(name)
        if pipeline:
            return pipeline.run(message_data)
        else:
            raise ValueError(f"Pipeline {name} not found")