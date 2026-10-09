# ---------------------------------------------------------
# Assignment 1 - Q4
# Exception-Safe CSV Transaction Splitter
# ---------------------------------------------------------

import csv
from datetime import datetime


def validate_transaction(row):
    """
    Validate one transaction row.

    Returns:
        (True, "") if valid
        (False, reason) if invalid
    """

    required_fields = ["tid", "acc", "type", "amount", "time"]

    # Check all required columns
    for field in required_fields:
        if field not in row or not row[field].strip():
            return False, f"Missing {field}"

    transaction_type = row["type"].strip().upper()

    # Check transaction type
    if transaction_type not in ("CREDIT", "DEBIT"):
        return False, "Invalid transaction type"

    # Check amount
    try:
        amount = float(row["amount"])
    except ValueError:
        return False, "Amount is not numeric"

    if amount <= 0:
        return False, "Amount must be greater than zero"

    # Check timestamp format
    try:
        datetime.strptime(
            row["time"].strip(),
            "%Y-%m-%dT%H:%M:%S"
        )
    except ValueError:
        return False, "Invalid timestamp"

    return True, ""


def process_file(filename):
    """Read and process the transaction CSV file."""

    balances = {}

    try:
        with open(filename, "r", newline="", encoding="utf-8") as infile:

            reader = csv.DictReader(infile)

            required = {"tid", "acc", "type", "amount", "time"}

            if not reader.fieldnames or not required.issubset(
                set(reader.fieldnames)
            ):
                print("Invalid CSV header.")
                return

            # Open output files
            with open(
                "credit.csv", "w", newline="", encoding="utf-8"
            ) as credit_file, \
            open(
                "debit.csv", "w", newline="", encoding="utf-8"
            ) as debit_file, \
            open(
                "error.csv", "w", newline="", encoding="utf-8"
            ) as error_file:

                credit_writer = csv.DictWriter(
                    credit_file,
                    fieldnames=reader.fieldnames
                )

                debit_writer = csv.DictWriter(
                    debit_file,
                    fieldnames=reader.fieldnames
                )

                error_fields = reader.fieldnames + ["reason"]

                error_writer = csv.DictWriter(
                    error_file,
                    fieldnames=error_fields
                )

                credit_writer.writeheader()
                debit_writer.writeheader()
                error_writer.writeheader()

                # Process every row independently
                for row in reader:

                    try:
                        valid, reason = validate_transaction(row)

                        if not valid:
                            row_with_error = row.copy()
                            row_with_error["reason"] = reason
                            error_writer.writerow(row_with_error)
                            continue

                        account = row["acc"].strip()
                        transaction_type = row["type"].strip().upper()
                        amount = float(row["amount"])

                        # Initialize account balance
                        balances.setdefault(account, 0)

                        if transaction_type == "CREDIT":
                            credit_writer.writerow(row)
                            balances[account] += amount

                        else:
                            debit_writer.writerow(row)
                            balances[account] -= amount

                    except Exception as error:
                        # Processing continues even if one row fails
                        row_with_error = row.copy()
                        row_with_error["reason"] = str(error)
                        error_writer.writerow(row_with_error)

    except FileNotFoundError:
        print("Input file not found.")
        return

    except Exception as error:
        print("Error:", error)
        return

    # Sort by absolute balance change, descending
    sorted_balances = sorted(
        balances.items(),
        key=lambda item: abs(item[1]),
        reverse=True
    )

    print("Account-wise balance changes:")

    for account, balance in sorted_balances:
        # Avoid displaying unnecessary .0
        if balance.is_integer():
            print(account, int(balance))
        else:
            print(account, balance)

    print("Files created: credit.csv, debit.csv, error.csv")


def main():

    filename = input("Enter CSV file path: ").strip()

    if not filename:
        print("File path cannot be empty.")
        return

    process_file(filename)


if __name__ == "__main__":
    main()