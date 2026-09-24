import datetime
import csv


class PolicyHolder:
    """Represents one policyholder's data."""
    def __init__(self, name, account_number):
        self.name = name
        self.account_number = account_number
        self.status = "active"
        self.date_joined = datetime.datetime.now().strftime("%Y-%m-%d")
        self.payments = []  # list of Payment objects/records

    def get_payments(self, payment_manager):
        """Pulls this holder's payments from the PaymentManager — always current."""
        return payment_manager.get_payments_for_holder(self.account_number)

    def display_details(self, payment_manager, product_manager):
        print(f"Name: {self.name}")
        print(f"Account Number: {self.account_number}")
        print(f"Status: {self.status}")
        print(f"Date Joined: {self.date_joined}")
        print("Payments:")
        payments = self.get_payments(payment_manager)
        if not payments:
            print("  (none)")
        for p in payments:
            product = product_manager.get_product(p.product_id)
            product_name = product.name if product else f"Unknown (id {p.product_id})"
            print(f"  - {product_name}: {p.amount} ({p.status}, due {p.due_date})")

    def to_dict(self):
        return {
            "name": self.name,
            "account_number": self.account_number,
            "status": self.status,
            "date_joined": self.date_joined,
        }


class PolicyManager:
    """Manages the collection of policyholders (register/suspend/reactivate)."""
    def __init__(self, filename="policy_holder_records.csv"):
        self.filename = filename
        self.holders = {}
        self._loaded = False

    def _ensure_loaded(self):
        if not self._loaded:
            self.load_from_csv(self.filename)
            self._loaded = True

    def load_from_csv(self, filename="policy_holder_records.csv"):
        try:
            with open(filename, "r", newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    account_number = int(row["account_number"])
                    holder = PolicyHolder(row["name"], account_number)
                    holder.status = row["status"]
                    holder.date_joined = row["date_joined"]
                    self.holders[account_number] = holder
        except FileNotFoundError:
            pass  # no file yet — nothing to load, that's fine

    def register(self, name, account_number):
        if account_number in self.holders:
            raise ValueError("Account number already exists")
        holder = PolicyHolder(name, account_number)
        self.holders[account_number] = holder
        return holder

    def suspend(self, account_number):
        self.holders[account_number].status = "suspended"

    def reactivate(self, account_number):
        self.holders[account_number].status = "active"

    def save_to_csv(self, filename="policy_holder_records.csv"):
        with open(filename, "w", newline="") as csvfile:
            fieldnames = ["name", "account_number", "status", "date_joined"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for holder in self.holders.values():
                writer.writerow(holder.to_dict())

