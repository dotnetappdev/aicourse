# Module 23 — Vision AI: Licence Plate Detection (ANPR) & Tax Check
**~8 min · Vision AI**

---

## Script

**Host:**
ANPR — Automatic Number Plate Recognition — reads the text on a vehicle's licence plate. Combined with a public DVLA API, we can check whether a UK vehicle has valid road tax. Everything runs locally except the final tax lookup, which hits a free government API.

> ⚠️ **Legal & ethical note**: Only check vehicles you own, or where you have clear permission. The DVLA API is a legitimate public service; misusing it (e.g. bulk queries on plates you don't own) may violate its terms of service.

### Step 1 — Read the Plate with LLaVA

```python
import ollama

def read_plate(image_path: str, model: str = "llava") -> str:
    """Extract the licence plate text from a vehicle image."""
    prompt = """Look at this vehicle image.
Find the licence plate (number plate) and read the text on it exactly.
Return ONLY the plate text, no explanation, no punctuation.
If you cannot see a plate, return: UNREADABLE
Example outputs: AB12CDE  or  UNREADABLE"""

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}]
    )
    plate = response["message"]["content"].strip().upper()
    plate = "".join(c for c in plate if c.isalnum())   # strip spaces/punctuation
    return plate
```

### Step 2 — Normalise the Plate

UK plates use the format `AA99 AAA`. We normalise before sending to the API:

```python
import re

def normalise_uk_plate(raw: str) -> str | None:
    """
    Normalise a raw plate string for the DVLA API.
    Returns the clean plate string, or None if format is not recognised.
    Supports current (AA99AAA) and older formats.
    """
    clean = raw.upper().replace(" ", "")

    patterns = [
        r"^[A-Z]{2}\d{2}[A-Z]{3}$",    # current: AB12CDE
        r"^[A-Z]\d{1,3}[A-Z]{3}$",      # prefix: A123BCD
        r"^[A-Z]{3}\d{1,3}[A-Z]$",      # suffix: ABC123D
        r"^[A-Z]{1,2}\d{1,4}$",         # dateless: AB1234
    ]
    for pattern in patterns:
        if re.match(pattern, clean):
            return clean
    return None
```

### Step 3 — DVLA Vehicle Enquiry API

The UK government provides a free Vehicle Enquiry Service API. You need a free API key from [developer-portal.driver-vehicle-licensing.api.gov.uk](https://developer-portal.driver-vehicle-licensing.api.gov.uk).

```python
import os, requests
from dotenv import load_dotenv

load_dotenv()
DVLA_API_KEY = os.getenv("DVLA_API_KEY", "")
DVLA_URL     = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"

def check_vehicle_tax(plate: str) -> dict:
    """
    Query the DVLA Vehicle Enquiry Service for tax and MOT status.

    Requires a DVLA_API_KEY environment variable.
    See: https://developer-portal.driver-vehicle-licensing.api.gov.uk
    """
    if not DVLA_API_KEY:
        return {"error": "DVLA_API_KEY not set. Add it to your .env file."}

    headers = {
        "x-api-key":    DVLA_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {"registrationNumber": plate}

    try:
        resp = requests.post(DVLA_URL, json=payload, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            return {"error": f"Plate {plate!r} not found in DVLA database."}
        return {"error": f"DVLA API error: {e}"}
    except requests.RequestException as e:
        return {"error": f"Network error: {e}"}
```

### Step 4 — Display the Result

```python
from rich.console import Console
from rich.panel   import Panel

console = Console()

def display_vehicle_info(plate: str, data: dict) -> None:
    """Render vehicle tax/MOT info in the terminal."""
    if "error" in data:
        console.print(f"[red]Error:[/red] {data['error']}")
        return

    tax_status = data.get("taxStatus", "Unknown")
    tax_due    = data.get("taxDueDate", "Unknown")
    mot_status = data.get("motStatus", "Unknown")
    mot_exp    = data.get("motExpiryDate", "Unknown")
    make       = data.get("make", "Unknown")
    colour     = data.get("colour", "Unknown")
    year       = data.get("yearOfManufacture", "Unknown")

    tax_colour  = "green"  if tax_status == "Taxed"    else "red"
    mot_colour  = "green"  if mot_status == "Valid"    else "red"

    console.print(Panel(
        f"[bold]Plate:[/bold]     {plate}\n"
        f"[bold]Make:[/bold]      {make}\n"
        f"[bold]Colour:[/bold]    {colour}\n"
        f"[bold]Year:[/bold]      {year}\n\n"
        f"[bold]Tax Status:[/bold]  [{tax_colour}]{tax_status}[/{tax_colour}]  (due: {tax_due})\n"
        f"[bold]MOT Status:[/bold]  [{mot_colour}]{mot_status}[/{mot_colour}]  (exp: {mot_exp})",
        title=f"[cyan]Vehicle Enquiry — {plate}[/cyan]",
        border_style="cyan",
    ))
```

### Putting It All Together

```python
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python anpr.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    console.print("[bold]Step 1:[/bold] Reading plate with LLaVA...")
    raw_plate = read_plate(image_path)
    console.print(f"  Raw OCR result: [yellow]{raw_plate}[/yellow]")

    plate = normalise_uk_plate(raw_plate)
    if not plate:
        console.print(f"[red]Could not parse a valid UK plate from: {raw_plate!r}[/red]")
        sys.exit(1)
    console.print(f"  Normalised plate: [bold green]{plate}[/bold green]")

    console.print("\n[bold]Step 2:[/bold] Checking DVLA database...")
    vehicle_data = check_vehicle_tax(plate)
    display_vehicle_info(plate, vehicle_data)
```

### Getting a DVLA API Key

1. Go to [developer-portal.driver-vehicle-licensing.api.gov.uk](https://developer-portal.driver-vehicle-licensing.api.gov.uk)
2. Create a free account
3. Subscribe to the "Vehicle Enquiry Service" API
4. Copy your API key into a `.env` file:

```
DVLA_API_KEY=your_key_here
```

---

## Practice

1. Find an image of a vehicle with a clearly visible UK plate (or use your own car).
2. Run the ANPR script and see if LLaVA reads the plate correctly.
3. (Optional) If the plate is slightly wrong, try re-prompting: "The plate starts with AB — re-read it carefully."
