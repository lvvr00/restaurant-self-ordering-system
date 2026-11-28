# Khmer Kitchen – Self-Ordering System

**Team**

| Member | Name | Responsibility |
|---|---|---|
| Member 1 | Chea Kimsorng | HTML/CSS front end |
| Member 2 | Veng Pichrachana | Welcome screen, menu data, reset |
| Member 3 | Chorn Thaliza | Shopping cart |
| Member 4 | Te Sopagna | Totals, receipt, payment |
| Member 5 | Rithy Lileakhena | Integration, testing, README |

---

## 1. Project Overview

Khmer Kitchen is a web-based self-ordering system for a small Cambodian restaurant. A customer uses a tablet placed on a table to look at the menu, add dishes to an order, review a receipt, and pay. 

The front end (what the customer sees) is built with HTML, CSS and JavaScript. The back end (the rules of the restaurant) is written in Python using the Flask framework. Keeping the rules in Python means prices, totals and validation are always calculated in one trusted place.

## 2. Features

- Welcome screen with **Order now** and **Exit** buttons
- Menu of 16 dishes in 4 categories, each with a photo and price
- Add a dish with a quantity and optional notes (for example "less spicy")
- Cart page: change quantity, edit notes, remove items, see the subtotal
- Total calculated as subtotal + 5% service charge + 10% tax
- Receipt showing order ID, table number, time, items, notes and totals
- Three payment methods: **Cash** (checks the amount and shows change), **Card** and **QR code** (both simulated)
- Confirmation message and automatic reset for the next customer
- Hidden staff option to stop the server
- Input validation and error messages for every step

## 3. Technologies Used

| Part | Technology |
|---|---|
| Back end | Python 3.9+, Flask |
| Front end | HTML5, CSS3, JavaScript (`fetch` to call the server) |
| Page templates | Jinja2 (included with Flask) |
| Testing | Python test script using Flask's test client |

## 4. The 12-Step Ordering Flow

| Step | What happens | Where in the project |
|---|---|---|
| 1 | Welcome screen | `templates/index.html` |
| 2 | Order or Exit (exit shows a goodbye message) | `index.html` + `static/app.js` |
| 3 | Show menu grouped by category with prices | `templates/menu.html` |
| 4 | Ordering loop: move between menu and cart until placing or cancelling | `menu.html`, `cart.html` |
| 5 | Add item: quantity must be a whole number greater than 0, notes optional | `logic.add_item()` |
| 6 | View and edit cart: change quantity, edit notes, remove, subtotal | `logic.edit_item()`, `remove_item()` |
| 7 | Place order: an empty cart is refused with a message | `logic.place_order()` |
| 8 | Calculate total: subtotal + service charge + tax | `logic.calculate_total()` |
| 9 | Receipt with order ID, table number, items, notes, total | `payment.html` |
| 10 | Payment: Cash, Card or QR | `logic.pay()` |
| 11 | Confirmation: "Payment/Order received. Order is being processed." | `logic.pay()` |
| 12 | Reset: cart cleared and return to the welcome screen | `logic.reset_session()` |

## 5. Project Structure

```
restaurant_app/
├── app.py            Flask server: one route per page + a JSON API
├── logic.py          All restaurant rules (menu, cart, totals, payment)
├── test_app.py       Automated edge-case tests
├── README.md        Short run instructions
├── templates/
│   ├── base.html     Shared layout (header, fonts, scripts)
│   ├── index.html    Welcome page
│   ├── menu.html     Menu page
│   ├── cart.html     Cart page
│   ├── checkout.html Order summary / place order
│   └── payment.html  Receipt and payment
└── static/
    ├── style.css     Colours, fonts and layout
    ├── app.js        Sends requests to Python and redraws the page
    └── images/       Food photos named by menu ID (N01.jpg, D05.jpg, ...)
```

### How the parts work together

```
Browser (HTML / CSS / JS)  <-- fetch() + JSON -->  app.py (Flask)  -->  logic.py
```

1. The browser loads a page from `templates/`.
2. When the customer presses a button, `app.js` sends a request to a `/api/...` address in `app.py`.
3. `app.py` passes the request to a function in `logic.py`.
4. `logic.py` checks the data, updates the cart and returns a result.
5. `app.py` sends the result back as JSON and `app.js` updates the page.

## 6. How to Run

**Requirements:** Python 3.9 or newer (https://www.python.org). On Windows, tick *Add Python to PATH* during installation.

1. Unzip the project folder.
2. Open a terminal inside the folder.
   - Windows: open the folder, click the address bar, type `cmd` and press Enter.
   - Mac: right-click the folder and choose *New Terminal at Folder*.
3. Install Flask (only once):
   ```
   pip install flask
   ```
4. Start the server:
   ```
   python app.py
   ```
   (On Mac use `python3 app.py` and `pip3 install flask` if the first versions do not work.)
5. Open Chrome and go to **http://127.0.0.1:5000**
6. To stop the server, click the terminal and press `Ctrl + C`.

**Common problems**

| Message | Fix |
|---|---|
| `python is not recognized` | Install Python again and tick *Add Python to PATH* |
| `No module named flask` | Run `pip install flask` |
| `Address already in use` | The server is already running in another window; close it |

## 7. How to Use

1. Press **order now**.
2. On the menu, press **Add** under a dish, choose a quantity and optional notes, then **Add to order**.
3. Press **VIEW ORDER** to open the cart. Use **+ / –**, **Notes** and **Remove** to edit it.
4. Press **checkout**, check the summary, then **place order**.
5. On the payment page, choose Cash, Card or QR and press **pay now**. For cash, type the amount given; the change is shown.
6. After the confirmation, the app returns to the welcome screen by itself after 10 seconds, or immediately with **start new order**.

**Staff option:** on the welcome screen, click the title 5 times quickly and enter the staff code to stop the server. The code is set as `STAFF_CODE` at the top of `logic.py`.

## 8. Settings

All settings are at the top of `logic.py`:

| Setting | Meaning | Value |
|---|---|---|
| `TABLE_NUMBER` | Table that owns this tablet | 7 |
| `STAFF_CODE` | Code for the hidden staff exit | see `logic.py` |
| `SERVICE_RATE` | Service charge | 0.05 (5%) |
| `TAX_RATE` | Tax | 0.10 (10%) |
| `MENU` | Dishes, prices and categories | 16 items |

To add a dish, copy one line in `MENU`, give it a new ID, name, price and category, and add a photo named with the same ID in `static/images/`. The menu page updates automatically after restarting the server.

## 9. Validation and Error Handling

The program checks the customer's input and shows a clear message instead of crashing:

| Situation | Result |
|---|---|
| Quantity is 0, negative, text or a decimal (e.g. 1.5) | Rejected: "Quantity must be a whole number" / "greater than 0" |
| Item ID is not on the menu | Rejected: "That item is not on the menu." |
| Invalid cart line number | Rejected: "Invalid item number." |
| Place order with an empty cart | Refused: "Your cart is empty." |
| Cash amount is blank, text or `nan` | Rejected: "Please enter a valid amount." |
| Cash is less than the total | Rejected, showing the total and the amount given |
| No payment method chosen | Rejected: "Please choose Cash, Card or QR." |
| Paying twice for the same order | Rejected: "This order has already been paid." |
| Cart changed after the receipt was made | Old receipt is discarded so the total is never out of date |
| Pressing *place order* twice | The same order ID is kept |
| Notes longer than 200 characters | Shortened to 200 characters |

## 10. Testing

The file `test_app.py` runs **40 automatic checks** covering every page, every API route and all the cases in Section 9, including correct totals and change.

```
python test_app.py
```

Expected last line: `All 40 checks passed`

Example calculation tested: 3 × $2.00 + 4 × $0.25 = $7.00 subtotal; service $0.35; tax $0.735; total ≈ $8.09.

## 11. Known Limitations

- **One tablet = one table = one customer at a time.** The cart is stored in the server's memory, so the system is designed to run on one computer for one table.
- **Card and QR payments are simulated.** The program always accepts them. Real card details must never be entered.
- **Orders are not saved.** Order IDs restart and order history is lost when the server stops, and the kitchen does not receive the order.
- The server is meant for local use (`http://127.0.0.1:5000`). It is not set up for publishing on the public internet.

## 12. Possible Future Improvements

- Save orders in a database (for example SQLite) so they are not lost
- A kitchen screen that shows new orders
- Real payment through an online payment provider
- Separate carts for many tables or customers at once
- Menu editing page for staff, and Khmer language option

## 13. Conclusion

This project shows how a restaurant ordering process can be built by separating the **interface** (HTML/CSS/JavaScript) from the **rules** (Python). Because all calculations and validation are in `logic.py`, the system is easy to test and easy to change, and each team member could work on a separate part and combine them through `app.py`.
