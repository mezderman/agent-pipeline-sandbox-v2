from typing import Literal
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
from tools.tool_schemas import tools
import json
from tools.refund_policy import get_refund_policy
from tools.transaction_details import get_transaction_details

load_dotenv()

messages = [
            {
                "role": "developer",
                "content": """ Analyze the user query and classify its intent.
                              Try to resolve the user request using the tools provided. generate step by step plan to respond to user request.
                         """
            }
        ]

class QueryAnalysis(BaseModel):
    intent: Literal["refund", "other"] = Field(
        ...,
        description="Classification of the query intent: either 'refund' or 'other'"
    )
    reason: str = Field(
        ...,
        description="Explanation of why the intent was classified this way"
    )

class FinalDecision(BaseModel):
    decision: Literal["refund_approved", "refund_denied"] = Field(
        ...,
        description="Final decision about refund"
    )
    reasoning: str = Field(
        ...,
        description="Explanation of why the decision was made"
    )

    steps: list[str] = Field(
        ...,
        description="List of steps you generated to resolve the user request"
    )

def analyze_query(client: OpenAI, user_message: str):
    messages.append({
        "role": "user",
        "content": user_message
    })
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=messages,
        response_format=QueryAnalysis
    )
    return completion

def plan_steps(client: OpenAI, user_message: str):
    messages.append({
        "role": "user",
        "content": user_message
    })
    completion = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=messages,
        tools=tools
    )
    
    return completion

def finalize_response(client: OpenAI):
    messages.append({
        "role": "developer",
        "content": """
                        analyze information in your context and make decision about refund. 
                        Customer has to meet all criteria in refund policy to be eligible for refund.
                        Be thorough and concise in your investigation. If customer didnt meet a refund criteria, deny refund. 
                              Only use the data provided by tools and your reasoning. Do not make up information 
                              Pay attention to all message metadata including dates, customer ID, and order information. Calculate the exact number of days that have passed from the purchase date to the refund request date.
                              All items in company refund policy must be true true and must be followed.
                              Provide your decision refund_approved or refund_denied and reasoning.
                              Final Decision:"""
    })
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=messages,
        response_format=FinalDecision
    )
    
    return completion

def load_message():
    try:
        with open("data/message.json", "r") as f:
            message_data = json.load(f)
            return message_data  # Return the entire message object
    except Exception as e:
        print(f"Error loading message: {e}")
        return None

# Example usage:
client = OpenAI()
message_data = load_message()
if message_data:
    # completion = analyze_query(client, json.dumps(message_data))
    # messages.append(completion.choices[0].message)
    # analyze_query = completion.choices[0].message.parsed
    # print(f"Analyze query: {analyze_query}")
    completion = plan_steps(client, json.dumps(message_data))
    response = completion.choices[0].message
else:
    print("Failed to load message from file")

if completion.choices[0].message.tool_calls:
        print("\n===. Processing Tool Calls ===")
        messages.append(completion.choices[0].message)  # Add assistant's message

        for tool_call in completion.choices[0].message.tool_calls:
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
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

# print("--------------------------------")
# print("after function calls")
# print("--------------------------------")
# print(messages)

final_decision = finalize_response(client)
print("--------------------------------")
print("Final response")
print("--------------------------------")
final_decision = final_decision.choices[0].message.parsed
print(f"Decision: {final_decision.decision}")
print(f"Reasoning: {final_decision.reasoning}")
print("\nSteps for resolution:")
for i, step in enumerate(final_decision.steps, 1):
    print(f"{i}. {step}")
