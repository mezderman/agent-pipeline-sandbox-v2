from core.task import Task
from openai import OpenAI
from tools.refund_policy import get_refund_policy
from tools.transaction_details import get_transaction_details
import json
from typing import Literal, List
from pydantic import BaseModel, Field
from core.utils import function_to_json

__CTX_VARS_NAME__ = "context_variables"


class FinalDecision(BaseModel):
    decision: Literal["refund_eligible", "refund_not_eligible"] = Field(
        ...,
        description="Final decision on whether the customer is eligible for a refund or not"
    )
    reason: str = Field(
        ...,
        description="Explanation of why the decision was made"
    )
    agents_steps: List[str] = Field(
        ...,
        description="Steps you took to resolve the refund request"
    )

class RefundTask(Task):
    def __init__(self, name, functions=[get_refund_policy, get_transaction_details]):
        self.name = name
        self.client = OpenAI()
        self.functions = functions
        
        # Register tools using parent method
        self.register_tools({
            "get_refund_policy": get_refund_policy,
            "get_transaction_details": get_transaction_details
        })

        self.tools = [function_to_json(f) for f in [get_refund_policy, get_transaction_details]]
        

    def process(self, data):
        print("Processing refund request...")
        super().process(data)
        messages = []
        new_messages = []
        completion = self.plan_resolution(self.client)

        tool_calls = completion.choices[0].message.tool_calls
        partial_response = self.handle_tool_calls(tool_calls, self.functions, completion.choices[0].message)

        new_messages.append(completion.choices[0].message)
        new_messages.extend(partial_response.messages)
        print(new_messages)

        final_decision_completion = self.final_decision(self.client, new_messages)
        final_decision = final_decision_completion.choices[0].message.parsed
       
       
        output_data = {
            **data,  # Spread existing input data
            "status": "completed",
            "decision": final_decision.decision,
            "reason": final_decision.reason,
            "agents_steps": final_decision.agents_steps
        }

        return output_data
    
    def plan_resolution(self, client: OpenAI):
        input_data = self.get_input_data()
        msg = [{
            "role": "developer",
            "content": f""" Analyze the user refund request:
                        Customer ID: {input_data['customer_id']}
                        Order ID: {input_data['order_id']}
                        Subject: {input_data['subject']}
                        Body: {input_data['body']} 
                        Message Date: {input_data['message_date']}
                        From Email: {input_data['from_email']}

                        Try to resolve the user request using the tools provided.generate step by step plan to resolve the request
                    """
        }]

        completion = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=msg,
            tools=self.tools
        )
        
        return completion
    

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
    
    
            
