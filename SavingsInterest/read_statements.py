import re
import PyPDF2
import datetime
from datetime import datetime
import send2trash
import os


def extract_current_value(lines):
    balance = [index for index, line in enumerate(lines) if "Closing balance" in line]
    balance_index = balance[0]
    current_values = {}
    for line in lines[balance_index + 1 :]:
        account_type, value = line.split("£")
        current_values[account_type.strip()] = float(
            "".join(x for x in value if x not in [" ", ","])
        )
    return current_values


def extract_current_rates(lines, interest_rates={}):
    for index, line in enumerate(lines):
        if "Interest rate as of" in line:
            interest_statement = line
            line_index = index
    try:
        if lines[line_index - 1] == "Boosted pots":
            pattern = r"\d+\.\d+"
            interest_31 = re.search(pattern, lines[line_index + 1])
            interest_rates["Boost 31"] = float(interest_31.group())
            interest_95 = re.search(pattern, lines[line_index + 2])
            interest_rates["Boost 95"] = float(interest_95.group())
        else:
            pattern = r"\d+\.\d+"
            interest_rate = re.search(pattern, interest_statement)
            interest_rates["Access"] = float(interest_rate.group())
    except:
        pass

    return interest_rates


def extract_interest(lines, interest_amount=0):
    for line in lines:
        if "Interest" in line and "£" in line:
            amount = "".join(x for x in line.split("£")[1] if x not in [" ", ","])
            interest_amount += float(amount)
    return round(interest_amount, 2)


def read_statement(filepath):
    f = open(filepath, "rb")

    pdf_reader = PyPDF2.PdfReader(f)

    interest_amount = 0
    for page in pdf_reader.pages:
        text = page.extract_text()
        lines = text.split("\n")

        interest_amount += extract_interest(lines)

    f.close()

    return interest_amount


def read_statement_current(filepath):
    f = open(filepath, "rb")

    pdf_reader = PyPDF2.PdfReader(f)

    interest_amount = 0

    page = pdf_reader.pages[0]
    text = page.extract_text()
    lines = text.split("\n")
    balance = extract_current_value(lines)

    for page in pdf_reader.pages[1:]:
        text = page.extract_text()
        lines = text.split("\n")
        interest_rates = extract_current_rates(lines)
        interest_amount += extract_interest(lines)

    f.close()

    return balance, interest_rates, interest_amount


def read_files_and_extract(tax_year):
    interest_amount = 0
    filedir = os.getcwd() + "\\statements"

    balance = {}
    interest_rates = {}
    for folder, sub_folders, files in os.walk(filedir):
        for file in files:
            if in_tax_year(file, tax_year):
                filepath = filedir + "/" + file
                # if tax_year == datetime.now().strftime("%Y"):
                if datetime.now().strftime("%B") in file:
                    (
                        balance,
                        interest_rates,
                        amount,
                    ) = read_statement_current(filepath)
                    send2trash.send2trash("statements/" + file)
                    print(f"Partial statement {file} has been deleted")
                else:
                    amount = read_statement(filepath)
                # else:
                #    amount = read_statement(filepath)
                interest_amount += amount

    return balance, interest_rates, interest_amount


def in_tax_year(filename, tax_year):
    tax_months_current = [
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    tax_months_next = ["January", "February", "March"]
    if tax_year in filename and any(month in filename for month in tax_months_current):
        return True
    elif str(int(tax_year) + 1) in filename and any(
        month in filename for month in tax_months_next
    ):
        return True
    else:
        return False
