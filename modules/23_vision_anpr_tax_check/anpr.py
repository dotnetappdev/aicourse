# anpr.py — Module 23
"""
Licence plate detection (ANPR) + UK DVLA tax/MOT check.

Requirements:
    pip install ollama requests rich python-dotenv
    ollama pull llava

Setup:
    Copy .env.example to .env and add your DVLA API key:
    https://developer-portal.driver-vehicle-licensing.api.gov.uk

Usage:
    python anpr.py vehicle.jpg

Legal note:
    Only query vehicles you own or have permission to check.
    The DVLA VES API is a legitimate public service for authorised use only.
"""

import os
import re
import sys
import pathlib

import requests
import ollama
from dotenv    import load_dotenv
from rich.console import Console
from rich.panel   import Panel

load_dotenv()

MODEL        = "llava"
DVLA_API_KEY = os.getenv("DVLA_API_KEY", "")
DVLA_URL     = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"

console = Console()


# ── Step 1: Read the plate with LLaVA ────────────────────────────────────

def read_plate(image_path: str) -> str:
    """
    Use LLaVA to OCR the licence plate in a vehicle image.

    Returns the plate text (alphanumeric only) or 'UNREADABLE'.
    """
    prompt = (
        "Look at this vehicle image. "
        "Find the licence plate (number plate) and read the characters on it exactly. "
        "Return ONLY the plate text with no spaces, no explanation. "
        "If you cannot see a plate clearly, return: UNREADABLE\n"
        "Examples of correct output: AB12CDE  or  UNREADABLE"
    )
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt, "images": [image_path]}],
    )
    raw   = response["message"]["content"].strip().upper()
    clean = "".join(c for c in raw if c.isalnum())
    return clean if clean else "UNREADABLE"


# ── Step 2: Normalise the plate ───────────────────────────────────────────

# UK plate format patterns (most common to least common)
_UK_PLATE_PATTERNS = [
    r"^[A-Z]{2}\d{2}[A-Z]{3}$",    # current (2001–):  AB12CDE
    r"^[A-Z]\d{1,3}[A-Z]{3}$",     # prefix  (1983–):  A123BCD
    r"^[A-Z]{3}\d{1,3}[A-Z]$",     # suffix  (1963–):  ABC123D
    r"^[A-Z]{1,3}\d{1,4}$",        # dateless:          AB1234
    r"^\d{1,4}[A-Z]{1,3}$",        # dateless (reversed)
]


def normalise_uk_plate(raw: str) -> str | None:
    """
    Normalise a raw OCR plate string.

    Returns the clean uppercase plate, or None if the format is unrecognised.
    """
    clean = raw.upper().replace(" ", "")
    for pattern in _UK_PLATE_PATTERNS:
        if re.match(pattern, clean):
            return clean
    return None


# ── Step 3: DVLA Vehicle Enquiry ──────────────────────────────────────────

def check_vehicle(plate: str) -> dict:
    """
    Query the DVLA Vehicle Enquiry Service API for tax and MOT status.

    Returns the API response dict, or a dict containing an "error" key.
    Requires DVLA_API_KEY to be set in the environment / .env file.
    See: https://developer-portal.driver-vehicle-licensing.api.gov.uk
    """
    if not DVLA_API_KEY:
        return {
            "error": (
                "DVLA_API_KEY is not set. "
                "Get a free key at https://developer-portal.driver-vehicle-licensing.api.gov.uk "
                "and add it to a .env file as: DVLA_API_KEY=your_key_here"
            )
        }

    headers = {
        "x-api-key":    DVLA_API_KEY,
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(
            DVLA_URL,
            json={"registrationNumber": plate},
            headers=headers,
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.HTTPError as exc:
        code = exc.response.status_code
        if code == 404:
            return {"error": f"Plate {plate!r} not found in DVLA database."}
        if code == 403:
            return {"error": "Invalid or expired DVLA API key."}
        return {"error": f"DVLA API returned HTTP {code}."}
    except requests.RequestException as exc:
        return {"error": f"Network error: {exc}"}


# ── Step 4: Display ───────────────────────────────────────────────────────

def display_result(plate: str, data: dict) -> None:
    """Render vehicle tax/MOT info in a Rich panel."""
    if "error" in data:
        console.print(f"[bold red]Error:[/bold red] {data['error']}")
        return

    tax_status = data.get("taxStatus",        "Unknown")
    tax_due    = data.get("taxDueDate",        "Unknown")
    mot_status = data.get("motStatus",         "Unknown")
    mot_exp    = data.get("motExpiryDate",     "Unknown")
    make       = data.get("make",              "Unknown")
    colour     = data.get("colour",            "Unknown")
    year       = data.get("yearOfManufacture", "Unknown")

    tax_col = "green" if tax_status == "Taxed"  else "red"
    mot_col = "green" if mot_status == "Valid"  else "red"

    console.print(Panel(
        f"[bold]Plate:[/bold]  {plate}\n"
        f"[bold]Make:[/bold]   {make}  |  "
        f"[bold]Colour:[/bold] {colour}  |  "
        f"[bold]Year:[/bold] {year}\n\n"
        f"[bold]Tax:[/bold]  [{tax_col}]{tax_status}[/{tax_col}]"
        f"  (due: {tax_due})\n"
        f"[bold]MOT:[/bold]  [{mot_col}]{mot_status}[/{mot_col}]"
        f"  (expires: {mot_exp})",
        title=f"[cyan]DVLA Vehicle Enquiry — {plate}[/cyan]",
        border_style="cyan",
    ))


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python anpr.py <vehicle_image>")
        sys.exit(1)

    image_path = sys.argv[1]
    if not pathlib.Path(image_path).exists():
        print(f"Error: file not found: {image_path}")
        sys.exit(1)

    # Step 1 — OCR the plate
    console.print("[bold]Step 1:[/bold] Reading plate with LLaVA...")
    raw = read_plate(image_path)
    console.print(f"  Raw OCR: [yellow]{raw}[/yellow]")

    if raw == "UNREADABLE":
        console.print("[red]Could not read a plate from this image.[/red]")
        sys.exit(1)

    plate = normalise_uk_plate(raw)
    if not plate:
        console.print(
            f"[red]Could not match a recognised UK plate format: {raw!r}[/red]\n"
            "Tip: try a clearer image or a closer crop of the plate."
        )
        sys.exit(1)

    console.print(f"  Plate: [bold green]{plate}[/bold green]")

    # Step 2 — DVLA lookup
    console.print("\n[bold]Step 2:[/bold] Querying DVLA...")
    vehicle_data = check_vehicle(plate)
    display_result(plate, vehicle_data)


if __name__ == "__main__":
    main()
