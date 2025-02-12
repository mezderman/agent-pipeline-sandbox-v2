from core.node import Node
from openai import OpenAI
from tools.refund_policy import get_refund_policy
from tools.transaction_details import get_transaction_details
from tools.tool_schemas import tools
import json
from typing import Literal, List
from pydantic import BaseModel, Field

class FinalDecision(BaseModel):
    decision: Literal["refund_eligible", "refund_not_eligible"] = Field(
        ...,
        description="Final decision on whether the customer is eligible for a refund or not"
    )
    reason: str = Field(
        ...,
        description="Explanation of why the decision was made"
    )
    steps: List[str] = Field(
        ...,
        description="Steps you took to resolve the refund request"
    )

class RefundNode(Node):
    def __init__(self, name):
        self.name = name
        self.client = OpenAI()

    def process(self, data):
        print("Processing refund request...")
        super().process(data)
        messages = []
        completion = self.plan_resolution(self.client)
        if completion.choices[0].message.tool_calls:    
            messages = self.execute_tools(completion.choices[0].message)
        else:
            print("No tool calls")

        final_decision_completion = self.final_decision(self.client, messages)
        final_decision = final_decision_completion.choices[0].message.parsed
       
        self.set_output_data({
            "status": "completed",
            "decision": final_decision.decision,
            "reason": final_decision.reason,
            "steps": final_decision.steps
        })

        return self.get_output_data()
    
    def plan_resolution(self, client: OpenAI):
        msg = [{
            "role": "developer",
            "content": """ Analyze the user refund request.
                        Try to resolve the user request using the tools provided.generate step by step plan to resolve the request
                    """
        }]

        completion = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=msg,
            tools=tools
        )
        
        return completion
    
    
    
    def execute_tools(self, message):
        messages = []
        messages.append(message)
        tool_calls = message.tool_calls
        for tool_call in tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            print(f"\n🔧 Executing tool: {name}")
            print(f"   Arguments: {args}")

            # Execute the appropriate tool
            result = globals()[name](**args)
            # if name == "get_refund_policy":
            #     result = get_refund_policy()
            # elif name == "get_transaction_details":
            #     result = get_transaction_details(**args)
            
            print(f"   Result received: {result is not None}")
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })
        return messages

    def final_decision(self,client: OpenAI, messages):
        msg = {
            "role": "developer",
            "content": """ Analyze the user refund request and the steps for resolution we generated.
                        Decide if the customer is eligible for a refund or not. explain your reasoning.
                        Make sure customer meet all the criteria for a refund.
                    """
        }
        messages.append(msg)
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=messages,
            response_format=FinalDecision
        )
        return completion
            
