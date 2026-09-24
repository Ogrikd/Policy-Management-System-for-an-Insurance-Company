import datetime
import csv

class Payment:
    """Represents a single payment record."""
    def __init__(self, account_number, product_id, amount, due_date):
        self.account_number = account_number
        self.product_id = product_id
        self.amount = amount
        self.due_date = due_date
        self.date_paid = None
        self.status = "pending"
        self.penalty = 0.0

    def to_dict(self):
        return {
            "account_number": self.account_number,
            "product_id": self.product_id,
            "amount": self.amount,
            "due_date": self.due_date,
            "date_paid": self.date_paid or "",
            "status": self.status,
            "penalty": self.penalty,
        }


class PaymentManager:
    """Handles processing, reminders, and penalties across all payments."""

    def __init__(self, penalty_rate=0.05, filename="payments.csv"):
        self.payments = []
        self.penalty_rate = penalty_rate
        self.filename = filename
        self._loaded = False

    def _ensure_loaded(self):
        if not self._loaded:
            self.load_from_csv(self.filename)
            self._loaded = True

    def load_from_csv(self, filename=None):
        filename = filename or self.filename
        try:
            with open(filename, "r", newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    payment = Payment(
                        int(row["account_number"]),
                        int(row["product_id"]),
                        float(row["amount"]),
                        row["due_date"],
                    )
                    payment.date_paid = row["date_paid"] or None
                    payment.status = row["status"]
                    payment.penalty = float(row["penalty"])
                    self.payments.append(payment)
        except FileNotFoundError:
            pass

    def save_to_csv(self, filename=None):
        filename = filename or self.filename
        fieldnames = ["account_number", "product_id", "amount",
                      "due_date", "date_paid", "status", "penalty"]
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for payment in self.payments:
                writer.writerow(payment.to_dict())

    def create_payment(self, account_number, product_id, amount, due_date):
        self._ensure_loaded()
        payment = Payment(account_number, product_id, amount, due_date)
        self.payments.append(payment)
        return payment

    def process_payment(self, payment):
        """Marks a payment as paid, applying any accrued penalty to the total."""
        if payment.status == "paid":
            raise ValueError("Payment already processed")
        total_due = payment.amount + payment.penalty
        payment.status = "paid"
        payment.date_paid = datetime.datetime.now().strftime("%Y-%m-%d")
        return total_due

    def send_reminder(self, payment):
        if payment.status != "pending":
            return None
        return (f"Reminder: payment of {payment.amount} for product {payment.product_id} "
                f"is due on {payment.due_date}.")

    def apply_penalty(self, payment, current_date=None):
        """Marks a pending payment overdue and applies a penalty if past due_date."""
        current_date = current_date or datetime.datetime.now().strftime("%Y-%m-%d")
        if payment.status == "pending" and current_date > payment.due_date:
            payment.status = "overdue"
            payment.penalty = round(payment.amount * self.penalty_rate, 2)
        return payment.penalty

    def get_payments_for_holder(self, account_number):
        return [p for p in self.payments if p.account_number == account_number]