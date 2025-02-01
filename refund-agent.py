from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import json
from openai import OpenAI
from dotenv import load_dotenv
import os

# Import tools
from tools.refund_policy import get_refund_policy
from tools.transaction_details import get_transaction_details
from tools.tool_schemas import tools

# Load environment variables
load_dotenv()
client = OpenAI()

# Pydantic models for structured data
class CustomerInfo(BaseModel):
    name: str
    email: str
    customer_id: str
    order_id: str
    refund_amount: float
    reason: str
    troubleshooting_steps: List[str]

class TransactionDetail(BaseModel):
    order_id: str
    product_name: str
    purchase_date: datetime
    amount: float
    status: str

class RefundRequest(BaseModel):
    customer_info: CustomerInfo
    transaction: Optional[TransactionDetail] = None
    meets_policy: Optional[bool] = None
    recommended_action: Optional[str] = None
    message_date: datetime

def main():
    print("\n=== 1. Loading Customer Message ===")
    try:
        with open("data/message.json", "r") as f:
            ticket = json.load(f)
        print("✅ Successfully loaded customer message")
    except Exception as e:
        print(f"❌ Error loading message: {e}")
        return

    print("\n=== 2. Preparing Initial Analysis ===")
    # System message with custom instructions
    messages = [
        {
            "role": "system",
            "content": """You are a customer service AI assistant handling refund requests. 
            Follow these steps:
            1. Analyze the customer's message and understand customer intent
            2. extract the key information from the message including message date
            3. Once you understand user intent, you must generate step by step plan to respond to user request. This plan should include the tools we should use to help us respond to user request
            4. After following the plan, analyze information in your context and make decision about refund
            6. All items in company refund policy are true and must be followed
            7. Provide your decision refund_approved or refund_denied and reasoning
            Final Decision:
            ===
            Decision:
            ===
            Reasoning:
            ===
            Always be thorough but concise in your analysis.
            
            
            """

            
        },
        {
            "role": "user",
            "content": f"Please analyze this customer message:\n\nFrom: {ticket['from']}\nCustomer ID: {ticket['customer_id']}\nmessage_date: {ticket['message_date']}\nSubject: {ticket['subject']}\nBody:\n{ticket['body']}"
        }
    ]

    print("\n=== 3. Calling OpenAI for Initial Analysis ===")
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0
        )
        print("✅ Received initial analysis from OpenAI")
    except Exception as e:
        print(f"❌ Error calling OpenAI: {e}")
        return

    print("\n=== Analysis Messages ===")
    print(f"messages: {completion.choices[0].message}")
    # Process tool calls if any
    if completion.choices[0].message.tool_calls:
        print("\n=== 4. Processing Tool Calls ===")
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
        
        print("\n=== 5. Getting Final Decision ===")
        try:
            final_completion = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0
            )
            print("✅ Received final decision")
        except Exception as e:
            print(f"❌ Error getting final decision: {e}")
            return

        print("\n=== 6. Final Response ===")
        final_response = final_completion.choices[0].message
        print("\n----- AI's Analysis and Decision -----")
        print(final_response.content)

if __name__ == "__main__":
    main()