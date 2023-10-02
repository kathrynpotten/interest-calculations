from savingsinterest import import_statements
from savingsinterest import read_statements
from savingsinterest import calculations
from savingsinterest import summary_email
import getpass


user = getpass.getpass("Email: ")
password = getpass.getpass("Password: ")

calculating = True

while calculating:
    tax_year = input("Which year would you like to calculate?: ")
    tax_band = input("Tax-band [20/40]: ")

    import_statements.import_statements_from_email(user, password)

    balance, interest_rates, interest_amount = read_statements.read_files_and_extract(
        tax_year
    )

    if balance:
        projected_simple = calculations.calculate_projected_simple(
            balance, interest_rates
        )
        projected_compound = calculations.calculate_projected_compound(
            balance, interest_rates
        )
        message = calculations.create_message(
            interest_amount,
            tax_band,
            tax_year,
            balance,
            interest_rates,
            projected_simple,
            projected_compound,
        )
    else:
        message = calculations.create_message(interest_amount, tax_band, tax_year)

    summary_email.send_summary_email(user, password, message)

    calculate_other = input("Calculate other tax-years? (y/n): ")
    if calculate_other == "y":
        continue
    else:
        break
