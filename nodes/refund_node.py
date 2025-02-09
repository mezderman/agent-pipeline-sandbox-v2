from core.node import Node
from core.memory import Memory
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
        self.memory = Memory()
        self.client = OpenAI()

    def process(self, data):
        print("Processing refund request...")
        self.set_input_data(data)
        completion = self.plan_resolution(self.client)
        self.memory.add_message({
            "role": "assistant",
            "content": completion.choices[0].message.content
        })
        if completion.choices[0].message.tool_calls:
            self.memory.add_message(completion.choices[0].message)
            self.execute_tools(completion.choices[0].message.tool_calls)
        else:
            print("No tool calls")

        final_decision_completion = self.final_decision(self.client)
        final_decision = final_decision_completion.choices[0].message.parsed
        msg={
            "role": "assistant",
            "content": f"""
                decision: {final_decision.decision}
                reason: {final_decision.reason}
                steps: {final_decision.steps}
            """
        }
        self.memory.add_message(msg)
        
        self.set_output_data({
            "status": "completed",
            "decision": final_decision.decision,
            "reason": final_decision.reason,
            "steps": final_decision.steps
        })

        return self.get_output_data()
    
    def plan_resolution(self, client: OpenAI):
        msg = {
            "role": "developer",
            "content": """ Analyze the user refund request.
                        Try to resolve the user request using the tools provided.generate step by step plan to resolve the request
                    """
        }
        self.memory.add_message(msg)

        completion = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=self.memory.get_messages(),
            tools=tools
        )
        
        return completion
    
    def execute_tools(self, tool_calls):
        for tool_call in tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            print(f"\n🔧 Executing tool: {name}")
            print(f"   Arguments: {args}")

            # Execute the appropriate tool
            if name == "get_refund_policy":
                result = get_refund_policy()
            elif name == "get_transaction_details":
                result = get_transaction_details(**args)
            
            print(f"   Result received: {result is not None}")

            # Add the result to messages
            self.memory.add_message({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })
        
        

    def final_decision(self,client: OpenAI):
        msg = {
            "role": "developer",
            "content": """ Analyze the user refund request and the steps for resolution we generated.
                        Decide if the customer is eligible for a refund or not. explain your reasoning.
                        Make sure customer meet all the criteria for a refund.
                    """
        }
        self.memory.add_message(msg)
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=self.memory.get_messages(),
            response_format=FinalDecision
        )
        return completion
            
