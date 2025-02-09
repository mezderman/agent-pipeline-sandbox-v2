class PipelineManager:
    def __init__(self):
        """Manages multiple pipelines."""
        self.pipelines = {}

    def register_pipeline(self, pipeline):
        """Registers a new pipeline."""
        self.pipelines[pipeline.name] = pipeline

    def run_pipeline(self, pipeline_name, data):
        """Executes a specified pipeline."""
        if pipeline_name in self.pipelines:
            return self.pipelines[pipeline_name].run(data, self)
        else:
            return f"Pipeline {pipeline_name} not found!"