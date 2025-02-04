from typing import List, Dict, Any
import json

class Memory:
    def __init__(self, system_prompt: str):
        self.messages: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]
    def add_developer_message(self, message: str):
        """Add a developer message to the conversation history"""
        self.messages.append({
            "role": "developer",
            "content": message
        })
        
    def add_user_message(self, message: str):
        """Add a user message to the conversation history"""
        self.messages.append({
            "role": "user",
            "content": message
        })

    def add_assistant_message(self, message: Any):
        """Add an assistant's message to the conversation history"""
        self.messages.append(message)

    def add_tool_result(self, tool_call_id: str, content: Any):
        """Add a tool's result to the conversation history"""
        self.messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": json.dumps(content)
        })

    def get_messages(self) -> List[Dict[str, str]]:
        """Get all messages in the conversation history"""
        return self.messages 