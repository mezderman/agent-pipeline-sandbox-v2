from core.node import Node
from openai import OpenAI
from tools.product_manual_rag import get_product_manual
from tools.product_manual_schema import product_manual_tools
from pydantic import BaseModel, Field
from typing import List

class FinalDecision(BaseModel):
    response: str = Field(
        ...,
        description="Response to the user's product issue"
    )
    agents_steps: List[str] = Field(
        ...,
        description="Steps you took to resolve the product issue"
    )

class ProductNode(Node):
    def __init__(self, name):
        self.name = name
        self.client = OpenAI()
        
        # Register tools
        self.register_tools({
            "get_product_manual": get_product_manual
        })

    def process(self, data):
        print("Processing product request...")
        super().process(data)
        
        # Convert Pydantic model to dict if necessary
        input_data = data.model_dump() if hasattr(data, 'model_dump') else data
        
        messages = []
        completion = self.plan_resolution(self.client)
        
        if completion.choices[0].message.tool_calls:    
            messages = self.execute_tools(completion.choices[0].message)
        else:
            print("No tool calls")

        final_decision_completion = self.final_decision(self.client, messages)
        final_decision = final_decision_completion.choices[0].message.parsed
       
       
        output_data = {
            **data,  # Spread existing input data
            "status": "completed",
            "response": final_decision.response,
            "agents_steps": final_decision.agents_steps
        }
        
        
        return output_data
        
    def plan_resolution(self, client: OpenAI):
        input_data = self.get_input_data()
        msg = [{
            "role": "developer",
            "content": f""" Analyze the user product issue:
                        Customer ID: {input_data['customer_id']}
                        Order ID: {input_data['order_id']}
                        Issue: {input_data['body']}
                        
                        Try to resolve the user's product issue using the product manual.
                        Generate a step by step plan to resolve the issue.
                    """
        }]

        completion = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=msg,
            tools=product_manual_tools
        )
        
        return completion 
    
    def final_decision(self, client: OpenAI, messages):
        msg = {
            "role": "developer",
            "content": """Analyze the user product issue and tools results and craft a response to the user that helps them with steps to resolve their issue.
                        Be specific and clear with the troubleshooting steps.
                        Make sure to address all aspects of their problem.
                        Format the response in a user-friendly way.
                    """
        }
        messages.append(msg)
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=messages,
            response_format=FinalDecision
        )
        return completion