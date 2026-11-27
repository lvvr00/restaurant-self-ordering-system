"""
Restaurant Ordering System
Covers: welcome screen, order/exit (+ hidden staff exit), menu data,
the main ordering loop, and session reset.
Functions marked TODO are placeholders for teammates to replace.
"""

import time 

TABLE_NUMBER = 7           # this tablet belongs to one table
STAFF_CODE = "staff123"    # hidden option on the Order/Exit screen

# Shared menu format: item ID -> details
MENU = {
    # Noodle Soups & Broths
    "N01": {"name": "Pork Noodle Soup", "price": 2.00, "category": "Noodle Soups & Broths"},
    "N02": {"name": "Beef Noodle Soup", "price": 2.00, "category": "Noodle Soups & Broths"},
    "N03": {"name": "Stir-Fried Short Rice Noodles/Lort Cha", "price": 2.00, "category": "Noodle Soups & Broths"},
    # Rice & Porridge Dishes
    "R01": {"name": "Grilled Pork & Rice", "price": 1.50, "category": "Rice & Porridge Dishes"},
    "R02": {"name": "Grilled Chicken & Rice", "price": 2.00, "category": "Rice & Porridge Dishes"},
    "R03": {"name": "Chicken Porridge", "price": 1.50, "category": "Rice & Porridge Dishes"},
    "R04": {"name": "White Porridge & Salted Egg", "price": 1.00, "category": "Rice & Porridge Dishes"},
    "R05": {"name": "Egg Fried Rice", "price": 1.50, "category": "Rice & Porridge Dishes"},
    "R06": {"name": "Shrimp Fried Rice", "price": 2.50, "category": "Rice & Porridge Dishes"},
    # Curry Noodles
    "C01": {"name": "Khmer Green Fish Curry Noodles", "price": 2.00, "category": "Curry Noodles"},
    "C02": {"name": "Red Chicken Curry Noodles", "price": 2.50, "category": "Curry Noodles"},
    # Drinks
    "D01": {"name": "Iced Milk Coffee", "price": 1.25, "category": "Drinks"},
    "D02": {"name": "Black Coffee", "price": 1.25, "category": "Drinks"},
    "D03": {"name": "Iced Lime Tea", "price": 1.25, "category": "Drinks"},
    "D04": {"name": "Soy Milk", "price": 0.75, "category": "Drinks"},
    "D05": {"name": "Water", "price": 0.25, "category": "Drinks"},
}

# Shared cart format: a list of dictionaries, one per item, e.g.
# {"id": "N02", "name": "Beef Noodle Soup", "price": 2.00, "qty": 2, "notes": "less spicy"}
cart = []


# ---------- Steps 1-3: welcome, order/exit, menu ----------

def welcome_screen():
    """Step 1: show the welcome screen."""
    print("\n" + "=" * 40)
    print(f"  Welcome! (Table {TABLE_NUMBER})")
    print("=" * 40)


def order_or_exit():
    """Step 2: returns 'order', 'exit', or 'staff_exit'."""
    while True:
        choice = input("\n1. Order\n2. Exit\nChoose: ").strip()
        if choice == "1":
            return "order"
        elif choice == "2":
            return "exit"
        elif choice == STAFF_CODE:
            return "staff_exit"
        print("Invalid choice. Please enter 1 or 2.")


def get_menu_by_category(menu):
    """Group menu items by category -> {category: [(id, item), ...]}.
    Returns data instead of printing, so the HTML page can reuse it."""
    grouped = {}
    for item_id, item in menu.items():
        grouped.setdefault(item["category"], []).append((item_id, item))
    return grouped


def show_menu(menu):
    """Step 3: print the menu by category."""
    print("\n=== MENU ===")
    for category, items in get_menu_by_category(menu).items():
        print(f"\n-- {category} --")
        for item_id, item in items:
            print(f"  {item_id}  {item['name']:<40} ${item['price']:.2f}")


# ---------- Step 4: main ordering loop ----------


def ordering_menu():
    """Repeats until the order is placed or cancelled.
    Returns 'placed' or 'cancelled'."""
    while True:
        print("\n--- ORDERING MENU ---")
        print("1. Add item\n2. View cart\n3. Remove/edit item")
        print("4. Place order\n5. Cancel order")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_item(cart, MENU)
        elif choice == "2":
            view_cart(cart)
        elif choice == "3":
            remove_item(cart)
        elif choice == "4":
            if place_order(cart):
                return "placed"
        elif choice == "5":
            if cancel_order(cart):
                return "cancelled"
        else:
            print("Invalid choice. Please enter 1-5.")


# ---------- Step 12: reset ----------

def reset_session():
    """Clear the cart so the next customer starts fresh."""
    cart.clear()


# ---------- Stubs for teammates ----------

def find_item(menu, name):
    """Look up an item by name (case-insensitive).
    Returns (real_name, price) or None if it does not exist."""
    name = str(name).strip().lower()
    for items in menu.values():
        for real_name, price in items.items():
            if real_name.lower() == name:
                return real_name, price
    return None


def validate_qty(qty):
    """Return (True, int_qty) if qty is a whole number > 0, else (False, error)."""
    try:
        q = int(str(qty).strip())
    except (ValueError, TypeError):
        return False, "Quantity must be a whole number."
    if q <= 0:
        return False, "Quantity must be greater than 0."
    return True, q


def _valid_index(cart, index):
    """index is 1-based (as shown to the customer)."""
    try:
        i = int(index)
    except (ValueError, TypeError):
        return None
    return i - 1 if 1 <= i <= len(cart) else None


def add_item(cart, menu, name, qty, notes=""):
    """Validate and add an item to the cart."""
    found = find_item(menu, name)
    if found is None:
        return False, f"'{name}' is not on the menu."
    real_name, price = found

    ok, q = validate_qty(qty)
    if not ok:
        return False, q

    notes = str(notes or "").strip()

    # same item + same notes -> just increase the quantity
    for line in cart:
        if line["name"] == real_name and line["notes"] == notes:
            line["qty"] += q
            return True, f"Updated {real_name}: now x{line['qty']}."

    cart.append({"name": real_name, "qty": q, "price": price, "notes": notes})
    return True, f"Added {q} x {real_name} to your cart."


def get_subtotal(cart):
    return round(sum(line["qty"] * line["price"] for line in cart), 2)


def view_cart(cart):
    """Return everything the frontend needs to display the cart."""
    lines = []
    for i, line in enumerate(cart, start=1):
        lines.append({
            "no": i,
            "name": line["name"],
            "qty": line["qty"],
            "price": line["price"],
            "notes": line["notes"],
            "line_total": round(line["qty"] * line["price"], 2),
        })
    return {"items": lines, "subtotal": get_subtotal(cart), "empty": not cart}


def edit_item(cart, index, qty=None, notes=None):
    """Change quantity and/or notes of the item at position `index` (1-based).
    Leave qty or notes as None to keep the old value."""
    i = _valid_index(cart, index)
    if i is None:
        return False, "Invalid item number."

    if qty is not None:
        ok, q = validate_qty(qty)
        if not ok:
            return False, q
        cart[i]["qty"] = q
    if notes is not None:
        cart[i]["notes"] = str(notes).strip()
    return True, f"Updated {cart[i]['name']}."


def remove_item(cart, index):
    """Remove the item at position `index` (1-based)."""
    i = _valid_index(cart, index)
    if i is None:
        return False, "Invalid item number."
    removed = cart.pop(i)
    return True, f"Removed {removed['name']} from your cart."


# ------------------------------------------------------- Step 7: empty check
def check_cart_before_order(cart):
    """Call this when the customer presses 'Place order'.
    ok == False means: show the message and go back to the ordering menu."""
    if not cart:
        return False, "Your cart is empty. Please add an item first."
    return True, "OK"


def cancel_order(cart):
    """Clear the cart (in place, so everyone's reference stays valid)."""
    cart.clear()
    return True, "Order cancelled. Your cart is now empty."


if __name__ == "__main__":
    MENU = {
        "Mains": {"Fried Rice": 3.50, "Beef Lok Lak": 5.00},
        "Drinks": {"Iced Coffee": 2.00},
    }
    cart = []

    print(check_cart_before_order(cart))                       # empty -> False
    print(add_item(cart, MENU, "fried rice", 2, "no egg"))     # ok
    print(add_item(cart, MENU, "Iced Coffee", "1"))            # ok (qty as text)
    print(add_item(cart, MENU, "Pizza", 1))                    # not on menu
    print(add_item(cart, MENU, "Fried Rice", 0))               # qty <= 0
    print(add_item(cart, MENU, "Fried Rice", "abc"))           # not a number
    print(add_item(cart, MENU, "Fried Rice", 1, "no egg"))     # merges -> x3
    print(edit_item(cart, 2, qty=4, notes="less ice"))
    print(edit_item(cart, 9, qty=1))                           # bad index
    print(view_cart(cart))
    print(remove_item(cart, 1))
    print("Subtotal:", get_subtotal(cart))
    print(check_cart_before_order(cart))                       # ok
    print(cancel_order(cart), cart)



SERVICE_RATE = 0.05    # 5% service charge
TAX_RATE = 0.10        # 10% tax
order_count = 0        # used to make order IDs


# Step 8: calculate total 

def calculate_total(cart):
    """Returns subtotal, service charge, tax and total."""
    subtotal = sum(i["price"] * i["qty"] for i in cart)
    service = subtotal * SERVICE_RATE
    tax = (subtotal + service) * TAX_RATE
    return {
        "subtotal": round(subtotal, 2),
        "service": round(service, 2),
        "tax": round(tax, 2),
        "total": round(subtotal + service + tax, 2),
    }


# Step 9: print receipt 

def generate_order_id():
    """Order ID like ORD-0001, ORD-0002, ..."""
    global order_count
    order_count += 1
    return f"ORD-{order_count:04d}"


def print_receipt(cart, totals, order_id):
    """Prints order ID, table number, items, notes and totals."""
    print("\n" + "=" * 40)
    print(f"Order ID : {order_id}")
    print(f"Table    : {TABLE_NUMBER}")
    print(f"Time     : {time.strftime('%Y-%m-%d %H:%M')}")
    print("-" * 40)
    for i in cart:
        line_total = i["price"] * i["qty"]
        print(f"{i['qty']} x {i['name']:<26} ${line_total:>6.2f}")
        if i.get("notes"):
            print(f"    Note: {i['notes']}")
    print("-" * 40)
    print(f"Subtotal        : ${totals['subtotal']:>8.2f}")
    print(f"Service ({SERVICE_RATE:.0%})    : ${totals['service']:>8.2f}")
    print(f"Tax ({TAX_RATE:.0%})        : ${totals['tax']:>8.2f}")
    print(f"TOTAL           : ${totals['total']:>8.2f}")
    print("=" * 40)


#Step 10: payment 

def pay_cash(total):
    """Asks for the amount tendered until it covers the total.
    Returns the change, or None if the customer goes back."""
    while True:
        entry = input(f"Total is ${total:.2f}. Enter amount tendered (or B to go back): ").strip()
        if entry.lower() == "b":
            return None
        try:
            paid = float(entry)
        except ValueError:
            print("Please enter a valid amount.")
            continue
        if paid < total:
            print(f"Not enough. Total is ${total:.2f}, you gave ${paid:.2f}.")
            continue
        change = round(paid - total, 2)
        print(f"Change: ${change:.2f}")
        return change


def payment(total):
    """Loops until the customer successfully pays by Cash, Card or QR."""
    while True:
        print("\n--- PAYMENT ---")
        print("1. Cash\n2. Card\n3. QR")
        choice = input("Choose: ").strip()
        if choice == "1":
            if pay_cash(total) is not None:
                return
        elif choice == "2":
            print("Processing card payment...")
            print("Card payment confirmed.")
            return
        elif choice == "3":
            print("Scan the QR code to pay...")
            print("QR payment confirmed.")
            return
        else:
            print("Invalid choice. Please enter 1-3.")


#Steps 8-11: checkout 

def checkout(cart):
    totals = calculate_total(cart)                   
    print_receipt(cart, totals, generate_order_id())
    payment(totals["total"])                         
    print("\nPayment/Order received. Order is being processed.")  


# ---------- Main program ----------

def main():
    while True:
        welcome_screen()
        action = order_or_exit()
        if action == "staff_exit":
            print("Shutting down. Goodbye!")
            break
        if action == "exit":
            print("Thank you! Goodbye.")
            continue
        show_menu(MENU)
        if ordering_menu() == "placed":
            checkout(cart)
        reset_session()


if __name__ == "__main__":
    main()
