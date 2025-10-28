import pdfplumber
import re
import pandas as pd

# Path to the uploaded PDF
pdf_path = "statement20251017.pdf"

data = []

# Regular expressions to capture the required fields
statement_date_pattern = re.compile(r"STATEMENT DATE:\s*([A-Z]{3}\s\d{1,2},\s\d{4})")
account_number_pattern = re.compile(r"GMI ACCOUNT NUMBER:\s*([A-Z0-9\s]+)")
account_value_pattern = pattern = re.compile(r"ACCOUNT VALUE AT MARKET\s*([^\r\n]+)")

# Open and read the PDF
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue

        # Check if page has "ACCOUNT VALUE AT MARKET"
        if "ACCOUNT VALUE AT MARKET" not in text:
            continue

        statement_date_match = statement_date_pattern.search(text)
        account_number_match = account_number_pattern.search(text)
        account_value_match = account_value_pattern.search(text)

        if all([statement_date_match, account_number_match, account_value_match]):
            data.append({
                "Statement Date": statement_date_match.group(1),
                "Account Number": account_number_match.group(1).strip().replace("\nSALESMAN", ""),
                "Account Value at Market": account_value_match.group(1).replace(",", "").split()[2].replace("-", "")
            })

pd.set_option('display.max_colwidth', None)   # show full column text
pd.set_option('display.max_rows', None)       # show all rows
pd.set_option('display.max_columns', None)    # show all columns

df = pd.DataFrame(data)

# Display extracted data
print(df)

