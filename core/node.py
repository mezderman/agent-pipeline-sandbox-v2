class Node:
    def __init__(self, name):
        """
        Initialize a Node with a name and a processing function.
        
        :param name: The name of the node.
        :param process_function: A function that defines the node's operation.
        """
        self.name = name

    def process(self, data):
        """
        Process the data using the node's processing function.
        
        :param data: The input data for the node.
        :return: The processed data.
        """
        print(f"Processing node: {self.name}")
        return data