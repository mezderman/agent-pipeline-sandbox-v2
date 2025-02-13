class Pipeline:
    def __init__(self, name):
        """Initialize an empty pipeline."""
        self.nodes = []
        self.dataLogger = []
        self.name = name
        self.inputData = []
        self.outputData = []

    def get_name(self):
        return self.name

    def add_node(self, node):
        self.nodes.append(node)
    
    def get_data_logger(self):
        return self.dataLogger
    
    def get_input_data(self):
        return self.inputData
    
    def get_output_data(self):
        return self.outputData
    
    def set_input_data(self, data):
        self.inputData = data
    
    def set_output_data(self, data):
        self.outputData = data

    def run(self, data):
        self.set_input_data(data)
        for node in self.nodes:
            node.set_input_data(data)
            data = node.process(data)
            node.set_output_data(data)
            self.dataLogger.append(data)
        self.set_output_data(data)
        return data
    
    