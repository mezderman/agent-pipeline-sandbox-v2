from pydantic import BaseModel, Field
from typing import Optional
from openai import OpenAI
import json

class PersonalInfo(BaseModel):
    first_name: str = Field(
        ...,
        description="User's first name"
    )
    last_name: str = Field(
        ...,
        description="User's last name"
    )

def collect_personal_info():
    client = OpenAI()
    personal_info = {}
    
    print("Hello, please enter your first and last name:")
    user_input = input().strip()
    
    # Try to parse first and last name from initial input
    msg = [
        {
            "role": "system",
            "content": """You are a helpful assistant collecting user's personal information. 
            Extract first name and last name from user input. Return them in a structured format."""
        },
        {
            "role": "user",
            "content": user_input
        }
    ]
    
    completion = do_completion(client, msg)
    
    personal_info = completion.choices[0].message.parsed
    
    # Check each field in the Pydantic model
    while True:
        missing_fields = False
        for field_name, field in PersonalInfo.model_fields.items():
            if not getattr(personal_info, field_name):
                missing_fields = True
                print(f"\nI am missing your {field_name.replace('_', ' ')}. Please enter it:")
                user_input = input().strip()
                msg.append({"role": "user", "content": f"My {field_name.replace('_', ' ')} is {user_input}"})
                
                completion = do_completion(client, msg)
                personal_info = completion.choices[0].message.parsed
        
        if not missing_fields:
            break

    print("\nThank you! I have all your information. Let's move to the next step!")
    return personal_info

def do_completion(client: OpenAI, messages):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=messages,
        response_format=PersonalInfo
    )
    return completion

def main():
    personal_info = collect_personal_info()
    print(f"\nCollected Information:")
    print(f"First Name: {personal_info.first_name}")
    print(f"Last Name: {personal_info.last_name}")

if __name__ == "__main__":
    main()
