from typing import Literal, List
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
from tools.tool_schemas import tools
import json
from tools.refund_policy import get_refund_policy
from tools.transaction_details import get_transaction_details
from core.memory import Memory
from core.Pipeline import Pipeline
from core.node import Node
from pipelines.analyze_query import AnalyzeQuery, QueryAnalysis


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
    

def load_message():
    try:
        with open("data/message.json", "r") as f:
            message_data = json.load(f)
            return message_data  # Return the entire message object
    except Exception as e:
        print(f"Error loading message: {e}")
        return None
    

def format_messages(messages):
    formatted = []
    for msg in messages:
        if hasattr(msg, 'model_dump'):
            formatted.append(msg.model_dump())
        else:
            formatted.append(msg)
    return formatted

def analyze_query(client: OpenAI):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=memory.get_messages(),
        response_format=QueryAnalysis
    )
    return completion


def plan_resolution(client: OpenAI):
    msg = {
        "role": "developer",
        "content": """ Analyze the user refund request.
                      Try to resolve the user request using the tools provided.generate step by step plan to resolve the request
                 """
    }
    memory.add_message(msg)
    completion = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=memory.get_messages(),
        tools=tools
    )
    
    return completion


def final_decision(client: OpenAI):
    msg = {
        "role": "developer",
        "content": """ Analyze the user refund request and the steps for resolution we generated.
                      Decide if the customer is eligible for a refund or not. explain your reasoning.
                      Make sure customer meet all the criteria for a refund.
                 """
    }
    memory.add_message(msg)
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=memory.get_messages(),
        response_format=FinalDecision
    )
    return completion

#step 1: analyze the query
load_dotenv()

message_data = load_message()
memory = Memory()
pipeline = Pipeline()
pipeline.add_node(AnalyzeQuery("Analyze Query Node"))
        

output = pipeline.run(message_data)
# print(output)
# completion = analyze_query(client)
# # messages.append(completion.choices[0].message)
# analyzed_query = completion.choices[0].message.parsed



# msg={
#         "role": "assistant",
#         "content": f"""
#             Intent: {analyzed_query.intent}
#         """
#     }

# memory.add_message(msg)

# # print("Messages:")
# # print(json.dumps(format_messages(messages), indent=2))
# if analyzed_query.intent == "refund_request":
#     #step 2: get refund policy
#     completion = plan_resolution(client)
#     memory.add_message({
#         "role": "assistant",
#         "content": completion.choices[0].message.content
#     })

#     # print(completion.choices[0].message.tool_calls)
   
#     if completion.choices[0].message.tool_calls:
#         memory.add_message(completion.choices[0].message) 
#         for tool_call in completion.choices[0].message.tool_calls:
#             name = tool_call.function.name
#             args = json.loads(tool_call.function.arguments)
            
#             print(f"\n🔧 Executing tool: {name}")
#             print(f"   Arguments: {args}")

#             # Execute the appropriate tool
#             if name == "get_refund_policy":
#                 result = get_refund_policy()
#             elif name == "get_transaction_details":
#                 result = get_transaction_details(**args)
            
#             print(f"   Result received: {result is not None}")

#             # Add the result to messages
#             memory.add_message({
#                 "role": "tool",
#                 "tool_call_id": tool_call.id,
#                 "content": json.dumps(result)
#             })
        
#     else:
#         print("No tool calls")

#     # print(json.dumps(format_messages(messages), indent=2))
   
#     completion = final_decision(client)
#     final_decision = completion.choices[0].message.parsed
#     # Assuming final_decision is an instance of FinalDecision
#     final_decision_dict = final_decision.dict()

#     # Print the final decision in a readable format
#     print(json.dumps(final_decision_dict, indent=2))
   
#     # print(messages)
# else:
#     print("Other")



