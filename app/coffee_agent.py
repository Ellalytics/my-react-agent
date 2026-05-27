from abc import ABC

from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel
from app.context_window import ContextWindow, UserMessage, AssistantMessage, ToolUse, ToolUseMessage, \
    ToolResultMessage
from app.claude_client import ClaudeClient

console = Console()


class Tool(BaseModel):
    name: str
    description: str
    input_schema: object


system_prompt = """You are an AI assistant that takes Coffee Orders for the popular café, Mamma's Coffee Shop.

Once you start chatting with a user, get their name, and check if they already exist in our system by using the get_customer_information tool.

If they do not exist, make sure to get their contact information (email or phone number).

Ask what sort of coffee they would like to order. You should ask about:
- Coffee type (Espresso, Cappuccino, Latte, Americano, Macchiato, etc.)
- Size (Small, Medium, Large)
- Any special requests (extra shot, oat milk, sugar, etc.)

Once you have all the information you need, use the create_coffee_order tool to place the order.

Once placed, let the user know their order number and that their coffee will be ready soon.
"""

tools = [
    Tool(
        name="get_customer_information",
        description="Get customer information from their name",
        input_schema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The customer's name"
                }
            },
            "required": ["name"]
        }
    ),
    Tool(
        name="create_coffee_order",
        description="Create a new coffee order for a customer",
        input_schema={
            "type": "object",
            "properties": {
                "coffee_description": {
                    "type": "string",
                    "description": "A description of the coffee to order, including type, size and special requests"
                },
                "contact_info": {
                    "type": "string",
                    "description": "Customer's contact information (email or phone number)"
                }
            },
            "required": ["coffee_description", "contact_info"]
        }
    )
]


class AgentInterface(ABC):
    def act(self) -> str:
        pass


class CoffeeAgent(AgentInterface):
    def __init__(
            self,
            context: ContextWindow,
            claude_client: ClaudeClient
    ):
        self.context = context
        self.claude_client = claude_client

    def send_message(self, user_message: str) -> str:
        self.context.add(UserMessage(content=user_message))
        response = self.act()
        self.context.add(AssistantMessage(content=response))
        return response

    def act(self) -> str:
        response = self.claude_client.send_messages_with_tools(
            messages=[msg.model_dump() for msg in self.context.conversation_history],
            tools=[tool.model_dump() for tool in tools]
        )

        if response.stop_reason == "tool_use":
            # Add tool use to context
            for content_block in response.content:
                if content_block.type == "tool_use":
                    # Add tool use message
                    tool_use = ToolUse(id="1", name=content_block.name, input=content_block.input)
                    tool_use_msg = ToolUseMessage(content=[tool_use])
                    self.context.add(tool_use_msg)
