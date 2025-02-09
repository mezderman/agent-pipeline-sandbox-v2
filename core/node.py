class Node:
    def __init__(self, name):
        """
        Initialize a Node with a name and a processing function.
        
        :param name: The name of the node.
        :param process_function: A function that defines the node's operation.
        """
        self.name = name
        self.inputData = []
        self.outputData = []

    def get_name(self):
        return self.name
    
    def get_input_data(self):
        return self.inputData
    
    def get_output_data(self):
        return self.outputData
    
    def set_input_data(self, data):
        self.inputData = data
    
    def set_output_data(self, data):
        self.outputData = data

    def process(self, data):
        """
        Process the data using the node's processing function.
        
        :param data: The input data for the node.
        :return: The processed data.
        """
        print(f"Processing node: {self.name}")
        return data