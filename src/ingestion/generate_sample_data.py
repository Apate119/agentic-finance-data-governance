from pathlib import Path
import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker


fake = Faker()
random.seed(42)
Faker.seed(42)

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


def random_date(start_date: datetime, end_date: datetime) -> datetime:
    """Return a random date between start_date and end_date."""
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    return start_date + timedelta(days=random_days)


def generate_customers(num_customers: int = 250) -> pd.DataFrame:
    customers = []

    for customer_id in range(1, num_customers + 1):
        customers.append(
            {
                "customer_id": f"CUST{customer_id:05d}",
                "customer_name": fake.company(),
                "customer_segment": random.choice(["Consumer", "Small Business", "Commercial", "Enterprise"]),
                "country": random.choice(["US", "US", "US", "CA", "GB"]),
                "created_date": random_date(datetime(2021, 1, 1), datetime(2025, 12, 31)).date(),
            }
        )

    df = pd.DataFrame(customers)

    # Intentional data quality issue: missing customer name
    df.loc[5, "customer_name"] = None

    return df


def generate_accounts(customers_df: pd.DataFrame, num_accounts: int = 400) -> pd.DataFrame:
    accounts = []

    customer_ids = customers_df["customer_id"].tolist()

    for account_id in range(1, num_accounts + 1):
        accounts.append(
            {
                "account_id": f"ACCT{account_id:06d}",
                "customer_id": random.choice(customer_ids),
                "account_type": random.choice(["Checking", "Savings", "Credit Card", "Loan"]),
                "account_status": random.choice(["Active", "Active", "Active", "Closed"]),
                "open_date": random_date(datetime(2021, 1, 1), datetime(2025, 12, 31)).date(),
            }
        )

    df = pd.DataFrame(accounts)

    # Intentional data quality issue: invalid customer_id
    df.loc[10, "customer_id"] = "CUST99999"

    return df


def generate_transactions(accounts_df: pd.DataFrame, num_transactions: int = 3000) -> pd.DataFrame:
    transactions = []

    account_ids = accounts_df["account_id"].tolist()

    for transaction_id in range(1, num_transactions + 1):
        transaction_type = random.choice(["Purchase", "Payment", "Fee", "Interest", "Transfer"])
        amount = round(random.uniform(5, 5000), 2)

        transactions.append(
            {
                "transaction_id": f"TXN{transaction_id:08d}",
                "account_id": random.choice(account_ids),
                "transaction_date": random_date(datetime(2025, 1, 1), datetime(2025, 12, 31)).date(),
                "transaction_type": transaction_type,
                "amount": amount,
                "currency": random.choice(["USD", "USD", "USD", "CAD", "GBP"]),
            }
        )

    df = pd.DataFrame(transactions)

    # Intentional data quality issues
    df.loc[25, "amount"] = -100.00
    df.loc[50, "account_id"] = "ACCT999999"

    # Duplicate transaction
    df = pd.concat([df, df.iloc[[100]]], ignore_index=True)

    return df


def generate_regulatory_balances(accounts_df: pd.DataFrame) -> pd.DataFrame:
    balances = []

    report_months = pd.date_range("2025-01-31", "2025-12-31", freq="ME")

    for report_date in report_months:
        for account_type in ["Checking", "Savings", "Credit Card", "Loan"]:
            balances.append(
                {
                    "report_date": report_date.date(),
                    "account_type": account_type,
                    "reported_balance": round(random.uniform(100000, 5000000), 2),
                    "report_name": random.choice(["FFIEC 031", "FR 2052a", "FR Y-9C"]),
                }
            )

    df = pd.DataFrame(balances)

    # Intentional data quality issue: missing reported balance
    df.loc[3, "reported_balance"] = None

    return df


def main() -> None:
    customers_df = generate_customers()
    accounts_df = generate_accounts(customers_df)
    transactions_df = generate_transactions(accounts_df)
    regulatory_balances_df = generate_regulatory_balances(accounts_df)

    customers_df.to_csv(RAW_DATA_DIR / "customers.csv", index=False)
    accounts_df.to_csv(RAW_DATA_DIR / "accounts.csv", index=False)
    transactions_df.to_csv(RAW_DATA_DIR / "transactions.csv", index=False)
    regulatory_balances_df.to_csv(RAW_DATA_DIR / "regulatory_balances.csv", index=False)

    print("Sample finance data generated successfully.")
    print(f"Files saved to: {RAW_DATA_DIR}")


if __name__ == "__main__":
    main()