# Policy Management System

A simple Python-based policy management system for an insurance company, built to manage policyholders, products, and payments.

## Overview

This project models three core parts of an insurance workflow, each with a data class and a manager class that handles operations on the collection:

| Domain | Record Class | Manager Class | Storage |
|---|---|---|---|
| Policyholders | `PolicyHolder` | `PolicyManager` | `policy_holder_records.csv` |
| Payments | `Payment` | `PaymentManager` | `payments.csv` |
| Products | `Product` | `ProductManager` | `products.csv` |

Each manager loads its data from its CSV file on first use and can save the current in-memory state back to disk on demand.

## Project Structure

```
policy_management_system/
├── policyholder.py      # PolicyHolder, PolicyManager
├── payment.py            # Payment, PaymentManager
├── product.py             # Product, ProductManager
├── main.py                # Demo script
├── .gitignore
└── README.md
```

## Features

### Policyholder Management (`policyholder.py`)
- `register(name, account_number)` — adds a new policyholder, rejecting duplicate account numbers
- `suspend(account_number)` — marks a policyholder as suspended
- `reactivate(account_number)` — restores a suspended policyholder to active status
- `display_details(payment_manager, product_manager)` — prints a holder's info along with their payment history

### Payment Management (`payment.py`)
- `create_payment(account_number, product_id, amount, due_date)` — creates a new payment record
- `process_payment(payment)` — marks a payment as paid, settling any accrued penalty
- `send_reminder(payment)` — returns a reminder message for a pending payment
- `apply_penalty(payment, current_date)` — flags an overdue payment and applies a penalty based on `penalty_rate`

### Product Management (`product.py`)
- `create_product(product_id, name, premium, description)` — adds a new product
- `update_product(product_id, ...)` — updates one or more fields on an existing product
- `suspend_product(product_id)` / `reactivate_product(product_id)` — toggles product availability without deleting history
- `remove_product(product_id)` — deletes a product entirely

## How Records Link Together

- `Payment.account_number` links a payment to a `PolicyHolder`.
- `Payment.product_id` links a payment to a `Product`.

Managers don't hold direct references to each other's objects — they're linked only by these IDs, which keeps each manager's data independently loadable and saveable from its own CSV file.

## Running the Demo

```bash
python main.py
```

`main.py` creates a product, registers two policyholders, makes and processes a payment for each against that product, prints both holders' account details (including their payment), and saves all three CSV files.

**Note:** Since `register()`, `create_payment()`, and `create_product()` check for duplicates against previously saved CSV data, running the script a second time without clearing the generated CSV files will raise a `ValueError` for the already-registered accounts and product. Delete `policy_holder_records.csv`, `payments.csv`, and `products.csv` between runs if you want a completely fresh demo.

## Requirements

- Python 3.x (uses only the standard library: `csv`, `datetime`)
