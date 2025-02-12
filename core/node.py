import json
from core.tool_registry import ToolRegistry

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
        print(f"Processing node: {self.name}")
        self.set_input_data(data)
        return data
    
    def execute_tools(self, message):
        messages = []
        messages.append(message)
        tool_registry = ToolRegistry.get_instance()
        
        for tool_call in message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            tool_function = tool_registry.get_tool(name)
            if tool_function:
                result = tool_function(**args)
                print(f"🔧 Executing tool: {name}")
            else:
                print(f"❌ Tool {name} not found!")
                continue
           
            print(f"   Result received: {result is not None}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })
        return messages

    def register_tools(self, tools: dict):
        registry = ToolRegistry.get_instance()
        for name, func in tools.items():
            registry.register_tool(name, func)