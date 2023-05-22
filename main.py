# Class to represent discount rules
class DiscountRule:
    def apply_discount(self, quantity, total_price):
        pass


class FlatDiscountRule(DiscountRule):
    def __init__(self, threshold, amount):
        self.threshold = threshold
        self.amount = amount

    def apply_discount(self, quantity, total_price):
        if sum(total_price.values()) > self.threshold:
            return self.amount
        return 0


class BulkDiscountRule(DiscountRule):
    def __init__(self, threshold, percent):
        self.threshold = threshold
        self.percent = percent

    def apply_discount(self, quantity, total_price):
        discount = 0
        for product, product_quantity in quantity.items():
            if product_quantity > self.threshold:
                discount += self.percent * total_price[product]
        return discount


class TieredDiscountRule(DiscountRule):
    def __init__(self, quantity_threshold, single_product_threshold, percent):
        self.quantity_threshold = quantity_threshold
        self.single_product_threshold = single_product_threshold
        self.percent = percent

    def apply_discount(self, quantity, total_price):
        discount = 0
        if sum(quantity.values()) > self.quantity_threshold:
            for product, product_quantity in quantity.items():
                if product_quantity > self.single_product_threshold:
                    quantity_above_threshold = product_quantity - self.single_product_threshold
                    discount += self.percent * (total_price[product] * quantity_above_threshold)
        return discount


# Catalog of products
catalog = {
    "Product A": 20,
    "Product B": 40,
    "Product C": 50
}

# Discount Rules
discount_rules = [
    FlatDiscountRule(threshold=200, amount=10),
    BulkDiscountRule(threshold=10, percent=0.05),
    BulkDiscountRule(threshold=20, percent=0.1),
    TieredDiscountRule(quantity_threshold=30, single_product_threshold=15, percent=0.5)
]

# Fees
gift_wrap_fee = 1
shipping_fee_per_package = 5
units_per_package = 10


# Function to display catalog
def display_catalog():
    print("Catalog:")
    for product, price in catalog.items():
        print(f"{product}\t\t${price}")


# Function to calculate shipping fee
def calculate_shipping_fee(total_quantity):
    return (total_quantity // units_per_package) * shipping_fee_per_package


# Function to calculate gift wrap fee
def calculate_gift_wrap_fee(total_quantity):
    return total_quantity * gift_wrap_fee


# Main program
def main():
    # Display catalog
    display_catalog()

    # Input quantities and gift wrapping preference
    quantity = {}
    for product in catalog:
        qty = int(input(f"Enter the quantity of {product}: "))
        quantity[product] = qty
    gift_wrapping = input("Would you like to wrap the products as gifts? (yes/no): ").lower() == "yes"

    # Calculate totals
    total_price = {product: catalog[product] * quantity[product] for product in catalog}

    subtotal = sum(total_price.values())

    # Apply discount rules and find the most beneficial discount
    applied_discount = None
    max_discount = 0
    for rule in discount_rules:
        discount = rule.apply_discount(quantity, total_price)
        if discount > max_discount:
            max_discount = discount
            applied_discount = rule

    shipping_fee = calculate_shipping_fee(sum(quantity.values()))
    gift_wrap_fee_total = calculate_gift_wrap_fee(sum(quantity.values()))

    total = subtotal - max_discount + shipping_fee + gift_wrap_fee_total
    if total < 0:
        total = 0

    # Output the details
    print("\n--- Purchase Details ---")
    for product in catalog:
        print(f"{product}: Quantity: {quantity[product]}, Total amount: ${total_price[product]}")
    print(f"\nSubtotal: ${subtotal}")
    if applied_discount:
        print(f"Discount Applied: {applied_discount.__class__.__name__} (${max_discount})")
    print(f"Shipping Fee: ${shipping_fee}")
    if gift_wrapping:
        print(f"Gift Wrap Fee: ${gift_wrap_fee_total}")
    print(f"Total: ${total}")


# Run the program
if __name__ == "__main__":
    main()