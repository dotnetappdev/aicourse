# rich_chat.py — Module 20 (Part B)
"""
Polished chatbot using the Rich library for beautiful terminal output.

Requirements:
    pip install ollama rich
    ollama pull llama3.2
"""

import ollama
from rich.console  import Console
from rich.panel    import Panel
from rich.markdown import Markdown
from rich.prompt   import Prompt

MODEL  = "llama3.2"
SYSTEM = (
    "You are a helpful AI assistant. "
    "Format responses with markdown: use **bold** for emphasis, "
    "bullet lists for multiple items, and code blocks for code."
)

console = Console()


def stream_and_render(messages: list) -> str:
    """Stream the LLM reply, then render it as markdown in a panel."""
    stream = ollama.chat(model=MODEL, messages=messages, stream=True)
    reply  = ""
    with console.status("[bold green]Thinking...[/]", spinner="dots"):
        for chunk in stream:
            reply += chunk["message"]["content"]

    console.print(
        Panel(Markdown(reply), title="[bold cyan]Assistant[/]", border_style="cyan")
    )
    return reply


def main():
    console.print(
        Panel(
            "[bold]Welcome to the AI Chat![/]\n"
            "Type [green]quit[/] to exit.",
            title="[bold magenta]Module 20 — Rich Chatbot[/]",
            border_style="magenta",
        )
    )

    history = [{"role": "system", "content": SYSTEM}]

    while True:
        user_input = Prompt.ask("\n[bold yellow]You[/]").strip()

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            console.print("[bold red]Goodbye![/]")
            break

        history.append({"role": "user", "content": user_input})
        reply = stream_and_render(history)
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
