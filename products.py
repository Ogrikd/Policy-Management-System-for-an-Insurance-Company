import csv


class Product:
    """Represents a single insurance policy product."""
    def __init__(self, product_id, name, premium, description=""):
        self.product_id = product_id
        self.name = name
        self.premium = premium
        self.description = description
        self.status = "active"  # active, suspended, removed

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "premium": self.premium,
            "description": self.description,
            "status": self.status,
        }


class ProductManager:
    def __init__(self, filename="products.csv"):
        self.products = {}  # product_id -> Product
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
                    product_id = int(row["product_id"])
                    product = Product(
                        product_id, row["name"],
                        float(row["premium"]), row["description"],
                    )
                    product.status = row["status"]
                    self.products[product_id] = product
        except FileNotFoundError:
            pass

    def save_to_csv(self, filename=None):
        filename = filename or self.filename
        fieldnames = ["product_id", "name", "premium", "description", "status"]
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for product in self.products.values():
                writer.writerow(product.to_dict())

    def create_product(self, product_id, name, premium, description=""):
        self._ensure_loaded()
        if product_id in self.products:
            raise ValueError(f"Product {product_id} already exists")
        product = Product(product_id, name, premium, description)
        self.products[product_id] = product
        return product

    def update_product(self, product_id, name=None, premium=None, description=None):
        product = self.products[product_id]
        if name is not None:
            product.name = name
        if premium is not None:
            product.premium = premium
        if description is not None:
            product.description = description
        return product

    def suspend_product(self, product_id):
        self.products[product_id].status = "suspended"

    def reactivate_product(self, product_id):
        self.products[product_id].status = "active"

    def remove_product(self, product_id):
        """Removes the product entirely rather than just suspending it."""
        del self.products[product_id]

    def get_product(self, product_id):
        return self.products.get(product_id)