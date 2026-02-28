# receipt_scanner.py — Module 22
"""
Scan a receipt photo and extract structured data using a local LLaVA model.

Requirements:
    pip install ollama rich
    ollama pull llava

Usage:
    python receipt_scanner.py receipt.jpg
"""

import json
import sys
import pathlib

import ollama
from rich.console import Console
from rich.panel   import Panel
from rich.table   import Table

MODEL   = "llava"
console = Console()

SYSTEM_PROMPT = (
    "You are a receipt data extractor. "
    "When given an image of a receipt, extract the information and return ONLY "
    "valid JSON. Never add explanation or text outside the JSON object."
)

EXTRACTION_PROMPT = """Extract all information from this receipt image.
Return ONLY valid JSON matching this exact structure:
{
  "merchant": "store name",
  "date": "YYYY-MM-DD or null",
  "items": [
    {"name": "item name", "quantity": 1, "unit_price": 0.00, "total": 0.00}
  ],
  "subtotal": 0.00,
  "tax": 0.00,
  "total": 0.00,
  "payment_method": "cash/card/contactless/unknown",
  "currency": "GBP"
}
Use null for any field you cannot read clearly."""


# ── Extraction ────────────────────────────────────────────────────────────

def scan_receipt(image_path: str) -> dict:
    """Extract structured data from a receipt image."""
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": EXTRACTION_PROMPT, "images": [image_path]},
        ],
        format="json",
    )
    return json.loads(response["message"]["content"])


# ── Validation ────────────────────────────────────────────────────────────

def validate_receipt(data: dict) -> list[str]:
    """Return a list of warnings for values that don't add up."""
    warnings  = []
    items_sum = sum(i.get("total", 0) or 0 for i in data.get("items", []))
    subtotal  = data.get("subtotal") or 0
    tax       = data.get("tax")      or 0
    total     = data.get("total")    or 0

    if subtotal > 0 and abs(items_sum - subtotal) > 0.10:
        warnings.append(
            f"Items sum ({items_sum:.2f}) ≠ subtotal ({subtotal:.2f})"
        )
    if total > 0 and subtotal > 0 and abs((subtotal + tax) - total) > 0.10:
        warnings.append(
            f"subtotal + tax ({subtotal + tax:.2f}) ≠ total ({total:.2f})"
        )
    return warnings


# ── Display ───────────────────────────────────────────────────────────────

def display_receipt(data: dict) -> None:
    """Render the extracted receipt in the terminal."""
    currency = data.get("currency") or ""
    merchant = data.get("merchant") or "Unknown Store"
    date     = data.get("date")     or "Unknown date"
    payment  = data.get("payment_method") or "Unknown"

    console.print(Panel(
        f"[bold]{merchant}[/bold]\n"
        f"Date:    {date}\n"
        f"Payment: {payment}",
        title="[cyan]Receipt Scanner[/cyan]",
        border_style="cyan",
    ))

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Item",       ratio=4)
    table.add_column("Qty",        justify="right")
    table.add_column("Unit Price", justify="right")
    table.add_column("Total",      justify="right", style="green")

    for item in data.get("items", []):
        table.add_row(
            item.get("name", "?"),
            str(item.get("quantity", 1)),
            f"{currency} {item.get('unit_price', 0):.2f}",
            f"{currency} {item.get('total', 0):.2f}",
        )

    console.print(table)
    console.print(f"Subtotal: {currency} {data.get('subtotal', 0):.2f}")
    console.print(f"Tax:      {currency} {data.get('tax', 0):.2f}")
    console.print(f"[bold green]Total:    {currency} {data.get('total', 0):.2f}[/bold green]")


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python receipt_scanner.py <receipt_image>")
        sys.exit(1)

    image_path = sys.argv[1]
    if not pathlib.Path(image_path).exists():
        print(f"Error: file not found: {image_path}")
        sys.exit(1)

    console.print(f"[bold]Scanning:[/bold] {image_path} ...")
    data = scan_receipt(image_path)

    display_receipt(data)

    warnings = validate_receipt(data)
    if warnings:
        console.print("\n[yellow]⚠ Validation warnings:[/yellow]")
        for w in warnings:
            console.print(f"  • {w}")


if __name__ == "__main__":
    main()
