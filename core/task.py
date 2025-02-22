import json
from core.types import Response

__CTX_VARS_NAME__ = "context_variables"

class Task:
    def __init__(self, name, functions=[]):

        self.name = name
        self.functions = functions
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
        print(f"Processing task: {self.name}")
        return data
    

    def handle_tool_calls(
        self,
        tool_calls,
        functions,
        context_variables,
    ):
        function_map = {f.__name__: f for f in functions}
        partial_response = Response(
            messages=[], context_variables={})

        for tool_call in tool_calls:
            name = tool_call.function.name
            # handle missing tool case, skip to next tool
            if name not in function_map:
                print(f"❌ Tool {name} not found in function map.")
                partial_response.messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "tool_name": name,
                        "content": f"Error: Tool {name} not found.",
                    }
                )
                continue
            args = json.loads(tool_call.function.arguments)
            print(f"🔧 Processing tool call: {name} with arguments {args}")

            func = function_map[name]
            # pass context_variables to agent functions
            if __CTX_VARS_NAME__ in func.__code__.co_varnames:
                args[__CTX_VARS_NAME__] = context_variables
            raw_result = function_map[name](**args)

            partial_response.messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": f'{raw_result}',
                    "tool_name": name
                }
            )

        return partial_response