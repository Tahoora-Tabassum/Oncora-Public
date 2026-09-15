import json
from pathlib import Path

import pandas as pd

# ==================================================
# Project Paths
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

EXCEL_FILE = PROJECT_ROOT / "data" / "Master_Database.xlsx"

OUTPUT_DIR = PROJECT_ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "chunks.json"

# ==================================================
# Read Workbook
# ==================================================

xls = pd.ExcelFile(EXCEL_FILE)

chunks = []
chunk_id = 1

# ==================================================
# Process Every Sheet
# ==================================================

for sheet in xls.sheet_names:

    print(f"Processing {sheet}...")

    # Read sheet normally
    df = pd.read_excel(EXCEL_FILE, sheet_name=sheet)

    # Remove completely empty rows/columns
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    # ------------------------------------------------
    # FIX "Unnamed" HEADERS
    # ------------------------------------------------
    # If pandas detected Unnamed columns, it means the
    # real header is probably the first row.
    # Promote first row to column names.
    # ------------------------------------------------

    unnamed_count = sum(str(col).startswith("Unnamed") for col in df.columns)

    if unnamed_count > len(df.columns) / 2:

        new_header = df.iloc[0]

        df = df[1:].reset_index(drop=True)

        df.columns = new_header

    # Remove empty rows again
    df = df.dropna(how="all")

    # ==================================================
    # Convert each row into one chunk
    # ==================================================

    for idx, row in df.iterrows():

        row = row.fillna("")

        metadata = {}

        text_lines = []

        for column, value in row.items():

            column = str(column).strip()
            value = str(value).strip()

            if value == "":
                continue

            metadata[column] = value

            text_lines.append(f"{column}: {value}")

        if not text_lines:
            continue

        chunks.append({

            "chunk_id": f"C{chunk_id:06d}",

            "sheet": sheet,

            "row_number": idx + 2,

            "text": "\n".join(text_lines),

            "metadata": metadata

        })

        chunk_id += 1

# ==================================================
# Save
# ==================================================

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    json.dump(chunks, f, indent=2, ensure_ascii=False)

print("=" * 60)
print("Chunk Generation Complete")
print("=" * 60)
print(f"Total Chunks : {len(chunks)}")
print(f"Saved To     : {OUTPUT_FILE}")

print("\nExample Chunk\n")
print(json.dumps(chunks[0], indent=2, ensure_ascii=False))