# ---------------------------------------------------------
# Assignment 1 - Q5
# Object-Oriented Bank Settlement System
# ---------------------------------------------------------


class BankError(Exception):
    """Base class for bank-related errors."""
    pass


class AccountNotFoundError(BankError):
    """Raised when an account does not exist."""
    pass


class InvalidAmountError(BankError):
    """Raised when amount is invalid."""
    pass


class InsufficientBalanceError(BankError):
    """Raised when withdrawal causes overdraft."""
    pass


class Account:
    """Represents one bank account."""

    def __init__(self, account_id, balance=0):
        self.account_id = account_id
        self._balance = balance

        # Transaction history for this account
        self._history = []

    @property
    def balance(self):
        """Getter for balance."""
        return self._balance

    def deposit(self, amount):
        """Deposit money into the account."""

        if amount <= 0:
            raise InvalidAmountError("Amount must be positive.")

        self._balance += amount

    def withdraw(self, amount):
        """Withdraw money without allowing overdraft."""

        if amount <= 0:
            raise InvalidAmountError("Amount must be positive.")

        if amount > self._balance:
            raise InsufficientBalanceError(
                f"Insufficient balance in {self.account_id}"
            )

        self._balance -= amount


class Transaction:
    """Stores information about a transaction."""

    def __init__(self, operation, account_from=None,
                 account_to=None, amount=0):
        self.operation = operation
        self.account_from = account_from
        self.account_to = account_to
        self.amount = amount

    def __str__(self):
        return (
            f"{self.operation}: "
            f"{self.account_from} -> {self.account_to} "
            f"{self.amount}"
        )


class Bank:
    """Manages accounts and transactions."""

    def __init__(self):
        self.accounts = {}
        self.history = []

    def add_account(self, account_id, balance):
        """Create a new account."""

        if balance < 0:
            raise InvalidAmountError(
                "Initial balance cannot be negative."
            )

        self.accounts[account_id] = Account(
            account_id,
            balance
        )

    def get_account(self, account_id):
        """Return account or raise an exception."""

        if account_id not in self.accounts:
            raise AccountNotFoundError(
                f"Account {account_id} does not exist."
            )

        return self.accounts[account_id]

    def deposit(self, account_id, amount):
        account = self.get_account(account_id)

        account.deposit(amount)

        transaction = Transaction(
            "DEPOSIT",
            account_to=account_id,
            amount=amount
        )

        self.history.append(transaction)

    def withdraw(self, account_id, amount):
        account = self.get_account(account_id)

        account.withdraw(amount)

        transaction = Transaction(
            "WITHDRAW",
            account_from=account_id,
            amount=amount
        )

        self.history.append(transaction)

    def transfer(self, from_id, to_id, amount):
        """Transfer money between two accounts."""

        source = self.get_account(from_id)
        destination = self.get_account(to_id)

        # Withdraw first.
        # If it fails, destination is never modified.
        source.withdraw(amount)
        destination.deposit(amount)

        transaction = Transaction(
            "TRANSFER",
            account_from=from_id,
            account_to=to_id,
            amount=amount
        )

        self.history.append(transaction)

    def snapshot(self):
        """
        Store current balances before a batch.
        This allows complete rollback.
        """

        return {
            account_id: account.balance
            for account_id, account in self.accounts.items()
        }

    def restore(self, snapshot):
        """Restore balances from a previous snapshot."""

        for account_id, balance in snapshot.items():
            self.accounts[account_id]._balance = balance


def main():

    bank = Bank()

    # -----------------------------------------------------
    # Read initial accounts
    # -----------------------------------------------------

    n = int(input().strip())

    for _ in range(n):
        account_id, balance = input().split()

        bank.add_account(
            account_id,
            int(balance)
        )

    # -----------------------------------------------------
    # Read operations
    # -----------------------------------------------------

    q = int(input().strip())

    batch_number = 0
    batch_snapshot = None
    failed_batches = []

    for _ in range(q):

        parts = input().split()

        if not parts:
            continue

        operation = parts[0]

        # -------------------------------------------------
        # Start batch
        # -------------------------------------------------

        if operation == "BATCH_BEGIN":

            batch_number += 1

            # Save balances before the batch begins
            batch_snapshot = bank.snapshot()

            continue

        # -------------------------------------------------
        # End batch
        # -------------------------------------------------

        if operation == "BATCH_END":

            batch_snapshot = None

            continue

        # -------------------------------------------------
        # Normal operation
        # -------------------------------------------------

        try:

            if operation == "DEPOSIT":

                account_id = parts[1]
                amount = int(parts[2])

                bank.deposit(account_id, amount)

            elif operation == "WITHDRAW":

                account_id = parts[1]
                amount = int(parts[2])

                bank.withdraw(account_id, amount)

            elif operation == "TRANSFER":

                from_id = parts[1]
                to_id = parts[2]
                amount = int(parts[3])

                bank.transfer(
                    from_id,
                    to_id,
                    amount
                )

            else:
                raise BankError("Unknown operation.")

        except BankError:

            # If operation belongs to a batch,
            # rollback the entire batch.
            if batch_snapshot is not None:

                bank.restore(batch_snapshot)

                failed_batches.append(batch_number)

                # Ignore remaining operations until BATCH_END.
                while True:

                    remaining = input().split()

                    if remaining and remaining[0] == "BATCH_END":
                        break

                batch_snapshot = None

    # -----------------------------------------------------
    # Output failed batches
    # -----------------------------------------------------

    for number in failed_batches:
        print(f"FAILED {number}")

    # -----------------------------------------------------
    # Print final balances in account ID order
    # -----------------------------------------------------

    for account_id in sorted(bank.accounts):

        balance = bank.accounts[account_id].balance

        print(account_id, balance)


if __name__ == "__main__":
    main()