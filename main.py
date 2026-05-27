from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from app.context_window import ContextWindow
from app.claude_client import ClaudeClient
from app.pizza_agent import PizzaAgent, system_prompt as pizza_prompt
from app.coffee_agent import CoffeeAgent, system_prompt as coffee_prompt

console = Console()

def select_agent():
    """Let user choose between Pizza or Coffee agent"""
    console.print(Panel.fit("🍕 Mamma's Business Suite 🍵", style="bold cyan"))
    console.print("\nSelect which service you'd like to use:\n", style="bold")
    console.print("  [bold green]1[/bold green] - 🍕 Pizza Delivery")
    console.print("  [bold blue]2[/bold blue] - ☕ Coffee Shop")
    console.print()
    
    while True:
        choice = console.input("[bold yellow]Your choice (1 or 2):[/bold yellow] ").strip()
        if choice == "1":
            return "pizza"
        elif choice == "2":
            return "coffee"
        else:
            console.print("[bold red]Invalid choice. Please enter 1 or 2.[/bold red]")

def main():
    # Select agent first
    agent_type = select_agent()
    
    if agent_type == "pizza":
        console.print(Panel.fit("🍕 Welcome to Mamma's Pizza Delivery Chat!", style="bold green"))
        system_prompt = pizza_prompt
        agent_class = PizzaAgent
    else:
        console.print(Panel.fit("☕ Welcome to Mamma's Coffee Shop!", style="bold blue"))
        system_prompt = coffee_prompt
        agent_class = CoffeeAgent
    
    console.print("Type [bold red]'quit'[/bold red] or [bold red]'exit'[/bold red] to end the conversation.", style="dim")
    console.print("─" * 60, style="dim")
    
    # Initialize the agent
    context = ContextWindow(conversation_history=[])
    claude_client = ClaudeClient(system_prompt=system_prompt)
    agent = agent_class(context=context, claude_client=claude_client)
    
    try:
        while True:
            # Get user input
            user_input = console.input("\n[bold blue]You:[/bold blue] ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                if agent_type == "pizza":
                    console.print("\n🍕 Thanks for choosing Mamma's Pizza! Goodbye!", style="bold green")
                else:
                    console.print("\n☕ Thanks for visiting Mamma's Coffee Shop! Goodbye!", style="bold blue")
                break
            
            # Skip empty inputs
            if not user_input:
                continue
            
            try:
                # Get agent response
                response = agent.send_message(user_input)
                console.print(f"\n🤖 [bold yellow]Agent:[/bold yellow] {response}")
                
            except Exception as e:
                console.print(f"\n❌ [bold red]Error:[/bold red] {str(e)}")
                console.print("[dim]Please try again.[/dim]")
                
    except KeyboardInterrupt:
        if agent_type == "pizza":
            console.print("\n\n🍕 Thanks for choosing Mamma's Pizza! Goodbye!", style="bold green")
        else:
            console.print("\n\n☕ Thanks for visiting Mamma's Coffee Shop! Goodbye!", style="bold blue")


if __name__ == "__main__":
    main()
