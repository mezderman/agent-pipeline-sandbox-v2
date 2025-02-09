class Pipeline:
    def __init__(self, name):
        """Initialize an empty pipeline."""
        self.nodes = []
        self.dataLogger = []
        self.name = name

    def get_name(self):
        return self.name

    def add_node(self, node):
        """
        Add a node to the pipeline.
        
        :param node: An instance of the Node class.
        """
        self.nodes.append(node)
    
    def get_data_logger(self):
        return self.dataLogger

    def run(self, data):
        """
        Run the pipeline with the given data.
        
        :param data: The initial input data for the pipeline.
        :return: The final output after processing through all nodes.
        """
        for node in self.nodes:
            data = node.process(data)
            self.dataLogger.append(data)
        return data