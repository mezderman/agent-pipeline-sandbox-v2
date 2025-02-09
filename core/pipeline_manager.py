class PipelineManager:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PipelineManager, cls).__new__(cls)
            cls._instance.pipelines = {}
            cls._instance.name = args[0] if args else None
        return cls._instance

    def __init__(self, name=None):
        if not hasattr(self, 'name'):
            self.name = name

    def register_pipeline(self, pipeline):
        """Register a pipeline with the manager"""
        self.pipelines[self.name] = pipeline

    def get_pipeline(self, name):
        """Get a pipeline by name"""
        return self.pipelines.get(name)
    
    def run_pipeline(self, pipeline_name, data):
        """Executes a specified pipeline."""
        if pipeline_name in self.pipelines:
            return self.pipelines[pipeline_name].run(data)
        else:
            return f"Pipeline {pipeline_name} not found!"