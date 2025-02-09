class Pipeline:
    def __init__(self):
        """Initialize an empty pipeline."""
        self.nodes = []

    def add_node(self, node):
        """
        Add a node to the pipeline.
        
        :param node: An instance of the Node class.
        """
        self.nodes.append(node)

    def run(self, data):
        """
        Run the pipeline with the given data.
        
        :param data: The initial input data for the pipeline.
        :return: The final output after processing through all nodes.
        """
        for node in self.nodes:
            data = node.process(data)
        return data