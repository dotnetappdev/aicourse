# Module 22 — Vision AI: Receipt Scanner
**~7 min · Vision AI**

---

## Script

**Host:**
Scanning a receipt is a perfect real-world use case for vision AI — it's messy, hand-written or printed in dozens of fonts, and you want structured data out. In this module we'll turn a photo of a receipt into clean JSON using a local LLaVA model.

### Why This Is Hard (Without AI)

Traditional OCR tools (like Tesseract) read text but don't *understand* it. They'd return a jumble of characters. You'd then need complex regex patterns per receipt format. With a multimodal LLM, you can describe what you want in plain English.

### The Core Approach

```python
import json, ollama

SYSTEM = """You are a receipt data extractor.
When given an image of a receipt, extract the data and return ONLY valid JSON.
Never add explanation outside the JSON."""

def scan_receipt(image_path: str) -> dict:
    """Extract structured data from a receipt image."""
    prompt = """Extract all information from this receipt image.
Return ONLY valid JSON with this structure:
{
  "merchant": "store name",
  "date": "YYYY-MM-DD or null",
  "items": [
    {"name": "item name", "quantity": 1, "unit_price": 0.00, "total": 0.00}
  ],
  "subtotal": 0.00,
  "tax": 0.00,
  "total": 0.00,
  "payment_method": "cash/card/unknown",
  "currency": "GBP/USD/etc"
}
Use null for any field you cannot read."""

    response = ollama.chat(
        model="llava",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user",   "content": prompt, "images": [image_path]}
        ],
        format="json",
    )
    return json.loads(response["message"]["content"])
```

### Displaying the Result

```python
from rich.console import Console
from rich.table   import Table
from rich.panel   import Panel

console = Console()

def display_receipt(data: dict) -> None:
    """Pretty-print extracted receipt data."""
    console.print(Panel(
        f"[bold]{data.get('merchant', 'Unknown Store')}[/bold]\n"
        f"Date: {data.get('date', 'Unknown')}\n"
        f"Payment: {data.get('payment_method', 'Unknown')}",
        title="[cyan]Receipt[/cyan]",
        border_style="cyan"
    ))

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Item",       style="white", ratio=4)
    table.add_column("Qty",        justify="right")
    table.add_column("Unit Price", justify="right")
    table.add_column("Total",      justify="right", style="green")

    currency = data.get("currency", "")
    for item in data.get("items", []):
        table.add_row(
            item.get("name", "?"),
            str(item.get("quantity", 1)),
            f"{currency} {item.get('unit_price', 0):.2f}",
            f"{currency} {item.get('total', 0):.2f}",
        )

    console.print(table)
    console.print(f"[bold]Subtotal:[/bold] {currency} {data.get('subtotal', 0):.2f}")
    console.print(f"[bold]Tax:[/bold]      {currency} {data.get('tax', 0):.2f}")
    console.print(f"[bold green]Total:[/bold green]    {currency} {data.get('total', 0):.2f}")
```

### Validating the Extracted Data

LLMs can make mistakes reading numbers. Always validate:

```python
def validate_receipt(data: dict) -> list[str]:
    """Return a list of warnings for suspicious values."""
    warnings = []

    items_sum = sum(i.get("total", 0) for i in data.get("items", []))
    subtotal  = data.get("subtotal", 0) or 0

    if subtotal > 0 and abs(items_sum - subtotal) > 0.10:
        warnings.append(
            f"Items sum ({items_sum:.2f}) doesn't match subtotal ({subtotal:.2f})"
        )

    total    = data.get("total",    0) or 0
    tax      = data.get("tax",      0) or 0

    if total > 0 and subtotal > 0 and abs((subtotal + tax) - total) > 0.10:
        warnings.append(
            f"subtotal + tax ({subtotal + tax:.2f}) doesn't match total ({total:.2f})"
        )

    return warnings
```

### Trying Multiple Images

```python
import sys

if len(sys.argv) < 2:
    print("Usage: python receipt_scanner.py receipt.jpg")
    sys.exit(1)

image_path = sys.argv[1]
data       = scan_receipt(image_path)
display_receipt(data)

warnings = validate_receipt(data)
if warnings:
    console.print("\n[yellow]⚠ Validation warnings:[/yellow]")
    for w in warnings:
        console.print(f"  • {w}")
```

---

## Practice

Take a photo of a real receipt (a supermarket or coffee shop receipt works well) and run it through the scanner. Try adjusting the prompt to improve accuracy — for example, explicitly mention the currency or ask the model to double-check totals.
