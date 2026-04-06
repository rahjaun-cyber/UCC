# =============================================================================
# Authors:      Lewis.Nathan - Forrester.Rahjaun
# Course:       ITT103 – Programming Techniques
# Purpose:      Point of Sale (POS) System for Best Buy Retail Store
# "I CERTIFY THAT I HAVE NOT GIVEN OR RECEIVED ANY UNAUTHORIZED ASSISTANCE
#  ON THIS ASSIGNMENT"
# =============================================================================

from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
TAX_RATE          = 0.10      # 10% sales tax
DISCOUNT_RATE     = 0.05      # 5% discount
DISCOUNT_THRESHOLD = 5000.00  # Discount applies when subtotal > $5,000
LOW_STOCK_LIMIT   = 5         # Alert threshold for low stock
STORE_NAME        = "Best Buy Retail Store"
STORE_ADDRESS     = "123 Market Street, Kingston, Jamaica"
STORE_PHONE       = "876-555-0199"

# ─────────────────────────────────────────────────────────────────────────────
# PRODUCT CATALOG  {product_name: {"price": float, "stock": int}}
# ─────────────────────────────────────────────────────────────────────────────
product_catalog = {
    "Kingston DDR5RAM 16gb(8x2)":     {"price": 350.00, "stock": 30},
    "Samsung Nvme SSD (8tb)":         {"price": 680.00, "stock": 20},
    " (2kg)":                         {"price": 420.00, "stock": 25},
    "nzxt Case (12L)":                {"price": 260.00, "stock": 18},
    "Corsair OLED Stream deck ":      {"price": 290.00, "stock": 15},
    "NVIDIA 4090 GPU (16Vram)":       {"price": 1250.00, "stock": 10},
    "Xbox eleit controller":          {"price": 310.00, "stock": 22},
    "Razer viper Ultimate ":          {"price": 195.00, "stock": 14},
    "Ducky 60% HE Keyboard":          {"price": 220.00, "stock": 12},
    "Skull Candy haedset":            {"price": 270.00, "stock": 40},
    "MH Wilds Steam activation Card": {"price": 120.00, "stock": 50},
    "ASUS TUFF 240 hrz 1440p":        {"price": 380.00, "stock": 8},
    "AMD RYZen 9070XTX (1kg)":        {"price": 2100.00, "stock": 6},
    "DDR5RAM 64gb(32each)":           {"price": 2490.00, "stock": 2},  # starts low for demo
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPER / UTILITY FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def format_currency(amount: float) -> str:
    """Return a nicely formatted currency string."""
    return f"${amount:,.2f}"


def get_positive_integer(prompt: str) -> int:
    """Prompt the user until they enter a valid positive integer."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("  ⚠  Please enter a number greater than zero.")
            else:
                return value
        except ValueError:
            print("  ⚠  Invalid input – please enter a whole number.")


def get_positive_float(prompt: str) -> float:
    """Prompt the user until they enter a valid positive float."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("  ⚠  Amount must be greater than zero.")
            else:
                return value
        except ValueError:
            print("  ⚠  Invalid input – please enter a numeric amount.")


def press_enter_to_continue():
    input("\n  Press ENTER to return to the main menu...")


# ─────────────────────────────────────────────────────────────────────────────
# DISPLAY FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def print_header(title: str):
    """Print a decorated section header."""
    width = 60
    print("\n" + "=" * width)
    print(f"  {title.upper()}")
    print("=" * width)


def display_main_menu():
    """Print the cashier main menu."""
    print_header("Best Buy POS – Main Menu")
    print("  [1]  View Product Catalog")
    print("  [2]  Add Item to Cart")
    print("  [3]  Remove Item from Cart")
    print("  [4]  View Cart")
    print("  [5]  Checkout / Process Payment")
    print("  [6]  New Transaction")
    print("  [0]  Exit")
    print("-" * 60)


def display_catalog():
    """Display the full product catalog with prices and stock."""
    print_header("Product Catalog")
    print(f"  {'#':<4} {'Product':<25} {'Price':>10}  {'Stock':>6}")
    print("  " + "-" * 50)
    for idx, (name, info) in enumerate(product_catalog.items(), start=1):
        stock_display = str(info['stock'])
        if info['stock'] < LOW_STOCK_LIMIT:
            stock_display += "  ⚠ LOW"
        print(f"  {idx:<4} {name:<25} {format_currency(info['price']):>10}  {stock_display:>6}")
    print()


def display_cart(cart: dict):
    """Display all items currently in the shopping cart."""
    print_header("Shopping Cart")
    if not cart:
        print("  The cart is empty.\n")
        return
    print(f"  {'Product':<25} {'Qty':>5}  {'Unit Price':>12}  {'Total':>12}")
    print("  " + "-" * 58)
    for name, details in cart.items():
        line_total = details["qty"] * details["unit_price"]
        print(f"  {name:<25} {details['qty']:>5}  "
              f"{format_currency(details['unit_price']):>12}  "
              f"{format_currency(line_total):>12}")
    print()


# ─────────────────────────────────────────────────────────────────────────────
# CART OPERATIONS
# ─────────────────────────────────────────────────────────────────────────────

def add_item_to_cart(cart: dict):
    """Interactively add a product to the cart."""
    display_catalog()
    product_names = list(product_catalog.keys())

    print("  Enter the product number to add (or 0 to cancel):")
    choice = get_positive_integer("  > ")

    if choice == 0:
        return

    if choice < 1 or choice > len(product_names):
        print("  ⚠  Invalid product number.")
        return

    product_name = product_names[choice - 1]
    available_stock = product_catalog[product_name]["stock"]

    if available_stock == 0:
        print(f"  ⚠  Sorry, '{product_name}' is currently out of stock.")
        return

    print(f"  Available stock for '{product_name}': {available_stock} unit(s).")
    qty = get_positive_integer("  Enter quantity: ")

    if qty > available_stock:
        print(f"  ⚠  Insufficient stock. Only {available_stock} unit(s) available.")
        return

    unit_price = product_catalog[product_name]["price"]

    if product_name in cart:
        # Product already in cart – increase quantity if stock allows
        new_qty = cart[product_name]["qty"] + qty
        if new_qty > available_stock:
            print(f"  ⚠  Cannot add {qty} more. Total would exceed available stock "
                  f"({available_stock} unit(s)).")
            return
        cart[product_name]["qty"] = new_qty
    else:
        cart[product_name] = {"qty": qty, "unit_price": unit_price}

    product_catalog[product_name]["stock"] -= qty

    print(f"  ✔  '{product_name}' × {qty} added to cart.")


def remove_item_from_cart(cart: dict):
    """Interactively remove a product (or reduce its quantity) from the cart."""
    if not cart:
        print("  ⚠  The cart is empty – nothing to remove.")
        return

    display_cart(cart)
    cart_items = list(cart.keys())

    print("  Enter the item number to remove (or 0 to cancel):")
    for idx, name in enumerate(cart_items, start=1):
        print(f"  [{idx}] {name}")

    choice = get_positive_integer("  > ")

    if choice == 0:
        return

    if choice < 1 or choice > len(cart_items):
        print("  ⚠  Invalid selection.")
        return

    product_name = cart_items[choice - 1]
    current_qty  = cart[product_name]["qty"]

    print(f"  Current quantity in cart: {current_qty}")
    print("  [1] Remove ALL units")
    print("  [2] Remove a specific number of units")
    sub = get_positive_integer("  > ")

    if sub == 1:
        del cart[product_name]
        product_catalog[product_name][("stock")] += current_qty
        print(f"  ✔  '{product_name}' removed from cart.")
    elif sub == 2:
        qty_to_remove = get_positive_integer("  Units to remove: ")
        if qty_to_remove >= current_qty:
            del cart[product_name]
            product_catalog[product_name]["qty"] += current_qty
            print(f"  ✔  '{product_name}' removed from cart.")
        else:
            cart[product_name]["qty"] -= qty_to_remove
            product_catalog[product_name]["stock"] += current_qty
            print(f"  ✔  Removed {qty_to_remove} unit(s). "
                  f"New quantity: {cart[product_name]['qty']}.")
    else:
        print("  ⚠  Invalid option.")


# ─────────────────────────────────────────────────────────────────────────────
# CALCULATION FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def calculate_subtotal(cart: dict) -> float:
    """Return the pre-tax, pre-discount subtotal."""
    return sum(item["qty"] * item["unit_price"] for item in cart.values())


def calculate_discount(subtotal: float) -> float:
    """Return the discount amount (5% if subtotal > $5,000, else 0)."""
    if subtotal > DISCOUNT_THRESHOLD:
        return round(subtotal * DISCOUNT_RATE, 2)
    return 0.0


def calculate_tax(amount_after_discount: float) -> float:
    """Return the sales tax (10%) on the discounted subtotal."""
    return round(amount_after_discount * TAX_RATE, 2)


def calculate_total(subtotal: float) -> tuple:
    """
    Given a raw subtotal, compute and return:
        (discount, tax, total_due)
    """
    discount          = calculate_discount(subtotal)
    discounted_amount = subtotal - discount
    tax               = calculate_tax(discounted_amount)
    total_due         = round(discounted_amount + tax, 2)
    return discount, tax, total_due


# ─────────────────────────────────────────────────────────────────────────────
# PAYMENT & RECEIPT
# ─────────────────────────────────────────────────────────────────────────────

def process_payment(total_due: float) -> float:
    """
    Prompt the cashier to enter the customer's payment.
    Validates that payment >= total_due.
    Returns the amount paid.
    """
    print(f"\n  Total Amount Due: {format_currency(total_due)}")
    while True:
        amount_paid = get_positive_float("  Enter amount received from customer: $")
        if amount_paid < total_due:
            print(f"  ⚠  Insufficient payment. Customer still owes "
                  f"{format_currency(total_due - amount_paid)}.")
        else:
            return round(amount_paid, 2)


def generate_receipt(cart: dict, subtotal: float, discount: float,
                     tax: float, total_due: float,
                     amount_paid: float, change: float,
                     transaction_id: int):
    """Print a formatted receipt to the console."""
    width  = 60
    border = "=" * width
    thin   = "-" * width
    now    = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")

    print("\n" + border)
    print(f"{'':^5}{STORE_NAME:^{width-5}}")
    print(f"  {STORE_ADDRESS}")
    print(f"  Tel: {STORE_PHONE}")
    print(thin)
    print(f"  Transaction #: {transaction_id:04d}       Date: {now}")
    print(thin)
    print(f"  {'ITEM':<26} {'QTY':>4}  {'UNIT':>9}  {'TOTAL':>10}")
    print(thin)

    for name, details in cart.items():
        line_total = details["qty"] * details["unit_price"]
        # Wrap long names
        display_name = name if len(name) <= 26 else name[:24] + ".."
        print(f"  {display_name:<26} {details['qty']:>4}  "
              f"{format_currency(details['unit_price']):>9}  "
              f"{format_currency(line_total):>10}")

    print(thin)
    print(f"  {'Subtotal':<40} {format_currency(subtotal):>12}")

    if discount > 0:
        print(f"  {'Discount (5% Loyalty)':<40} {format_currency(-discount):>12}")

    print(f"  {'Sales Tax (10%)':<40} {format_currency(tax):>12}")
    print(f"  {'TOTAL DUE':<40} {format_currency(total_due):>12}")
    print(thin)
    print(f"  {'Amount Paid':<40} {format_currency(amount_paid):>12}")
    print(f"  {'Change':<40} {format_currency(change):>12}")
    print(border)
    print(f"{'Thank You for Shopping at Best Buy!':^{width}}")
    print(f"{'Please Come Again :)':^{width}}")
    print(border + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# CHECKOUT FLOW
# ─────────────────────────────────────────────────────────────────────────────

def checkout(cart: dict, transaction_id: int) -> bool:
    """
    Run the full checkout process:
      1. Show cart summary
      2. Calculate totals
      3. Process payment
      4. Update stock2

      5. Print receipt
      6. Show low-stock warnings
    Returns True if checkout completed, False if cancelled.
    """
    if not cart:
        print("  ⚠  Your cart is empty. Please add items before checking out.")
        return False

    display_cart(cart)

    subtotal               = calculate_subtotal(cart)
    discount, tax, total_due = calculate_total(subtotal)

    print(f"  Subtotal : {format_currency(subtotal)}")
    if discount > 0:
        print(f"  Discount : {format_currency(-discount)}  (5% loyalty discount applied!)")
    print(f"  Tax (10%): {format_currency(tax)}")
    print(f"  TOTAL DUE: {format_currency(total_due)}")

    # Confirm before payment
    confirm = input("\n  Proceed to payment? (y/n): ").strip().lower()
    if confirm != 'y':
        print("  Checkout cancelled.")
        return False

    amount_paid = process_payment(total_due)
    change      = round(amount_paid - total_due, 2)

    # Update product stock


    generate_receipt(cart, subtotal, discount, tax, total_due,
                     amount_paid, change, transaction_id)

    # Low-stock alerts after transaction
    low_stock_items = [name for name, info in product_catalog.items()
                       if info["stock"] < LOW_STOCK_LIMIT]
    if low_stock_items:
        print("  ⚠  LOW STOCK ALERT – Please reorder the following items:")
        for item in low_stock_items:
            qty = product_catalog[item]["stock"]
            status = "OUT OF STOCK" if qty == 0 else f"{qty} unit(s) remaining"
            print(f"     • {item}: {status}")
        print()

    return True


# ─────────────────────────────────────────────────────────────────────────────
# MAIN PROGRAM LOOP
# ─────────────────────────────────────────────────────────────────────────────

def main():
    """Entry point – manages the session and routes cashier actions."""
    print("\n" + "=" * 60)
    print(f"  Welcome to {STORE_NAME}")
    print(f"  POS System  |  ITT103 – Spring 2026")
    print("=" * 60)

    cart           = {}
    transaction_id = 1

    while True:
        display_main_menu()
        choice = input("  Select an option: ").strip()

        if choice == "1":
            display_catalog()
            press_enter_to_continue()

        elif choice == "2":
            add_item_to_cart(cart)
            press_enter_to_continue()

        elif choice == "3":
            remove_item_from_cart(cart)
            press_enter_to_continue()

        elif choice == "4":
            display_cart(cart)
            press_enter_to_continue()

        elif choice == "5":
            completed = checkout(cart, transaction_id)
            if completed:
                transaction_id += 1
                cart = {}   # clear cart for next transaction
            press_enter_to_continue()

        elif choice == "6":
            if cart:
                confirm = input("  Clear current cart and start a new transaction? (y/n): ").strip().lower()
                if confirm == 'y':
                    cart = {}
                    print("  ✔  Cart cleared. Ready for new transaction.")
                else:
                    print("  New transaction cancelled.")
            else:
                print("  Cart is already empty. Ready for a new transaction.")
            press_enter_to_continue()

        elif choice == "0":
            print("\n  Closing POS System...")
            print(f"  Total transactions processed this session: {transaction_id - 1}")
            print("  Goodbye!\n")
            break

        else:
            print("  ⚠  Invalid option – please enter a number from the menu.")


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
