from pathlib import Path
import pandas as pd

# --------------------------------------------------
# Locate the project root automatically
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# --------------------------------------------------
# Excel file path
# --------------------------------------------------
EXCEL_FILE = PROJECT_ROOT / "data" / "Master_Database.xlsx"

# --------------------------------------------------
# Check if file exists
# --------------------------------------------------
if not EXCEL_FILE.exists():
    raise FileNotFoundError(f"\nExcel file not found:\n{EXCEL_FILE}")

print("=" * 60)
print("Cancer Nutrition AI")
print("Step 1 : Reading Master Database")
print("=" * 60)

# --------------------------------------------------
# Load workbook
# --------------------------------------------------
xls = pd.ExcelFile(EXCEL_FILE)

print(f"\nWorkbook Loaded Successfully")
print(f"Number of Sheets : {len(xls.sheet_names)}")

print("\nSheets Found:")

for i, sheet in enumerate(xls.sheet_names, start=1):
    print(f"{i}. {sheet}")

# --------------------------------------------------
# Read every sheet
# --------------------------------------------------
database = {}

print("\nLoading Sheets...\n")

for sheet in xls.sheet_names:

    df = pd.read_excel(EXCEL_FILE, sheet_name=sheet)

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove completely empty columns
    df = df.dropna(axis=1, how="all")

    database[sheet] = df

    print(
        f"{sheet:<25}"
        f" Rows: {len(df):<6}"
        f" Columns: {len(df.columns)}"
    )

print("\nAll sheets loaded successfully.")

# --------------------------------------------------
# Quick Preview
# --------------------------------------------------

print("\nPreview of First Sheet\n")

first_sheet = xls.sheet_names[0]

print(database[first_sheet].head())

print("\nFinished.")