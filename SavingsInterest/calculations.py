import datetime
from datetime import datetime
import dateutil.relativedelta


def calculate_projected_simple(balance, interest_rates):
    projected_interest = 0
    current_month = datetime.now().month
    months_remaining = 12 - current_month
    for account, value in balance.items():
        rate = interest_rates[account] * months_remaining / 12
        projected_interest += rate / 100 * value

    return round(projected_interest, 2)


def calculate_projected_compound(balance, interest_rates):
    projected_interest = 0
    current_month = datetime.now().month
    months_remaining = 12 - current_month
    for account, value in balance.items():
        rate = interest_rates[account] / 12
        for _ in range(months_remaining):
            interest = rate / 100 * value
            value += interest
            projected_interest += interest

    return round(projected_interest, 2)


def remaining_tax_free(tax_band, interest_amount):
    if tax_band == "20":
        remaining_tax_free = 1000 - interest_amount
    elif tax_band == "40":
        remaining_tax_free = 500 - interest_amount

    return remaining_tax_free


def create_message(
    interest_amount,
    tax_band,
    tax_year,
    balance={},
    interest_rates={},
    projected_simple=0,
    projected_compound=0,
):
    if tax_year == datetime.now().strftime("%Y"):
        remaining = remaining_tax_free(tax_band, interest_amount)
        if balance:
            balance_repr = "\n"
            for account, value in balance.items():
                balance_repr += f"\n{account}   {value}"
            rates_repr = "\n"
            for account, value in interest_rates.items():
                rates_repr += f"\n{account}   {value}"
            today = datetime.today().strftime("%Y-%m-%d")
            projected_year = round(projected_compound + interest_amount, 2)
            summary_message = f"""Your total interest for the current tax year at {today} is {interest_amount}.\nYou have {remaining} of tax-free interest remaining.\nYour current balance is: {balance_repr}, 
            \nwith interest rates: {rates_repr}.\n\nProjected interest for rest of tax-year with current balance and interest rates is {projected_simple} (simple), or {projected_compound} (compounded), giving total interest for tax-year of {projected_year}."""
            if remaining_tax_free(tax_band, projected_year) < 0:
                summary_message += (
                    "\nProjected to exceed tax limit. Consider moving savings to ISA."
                )
        else:
            last_month = (
                datetime.today() + dateutil.relativedelta.relativedelta(months=-1)
            ).strftime("%B")
            summary_message = f"""Your total interest for the current tax year at end of {last_month} is {interest_amount}.\nYou have {remaining} of tax-free interest remaining."""
    else:
        summary_message = (
            f"""Your total interest for tax year {tax_year} was {interest_amount}."""
        )

    return summary_message


if __name__ == "__main__":
    print(datetime.now().strftime("%B"))
    today = datetime.today()
    last_month = today + dateutil.relativedelta.relativedelta(months=-1)
    last_month = last_month.strftime("%B")
    print(last_month)
