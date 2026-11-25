"""Personal Expense Tracker - command-line application."""
import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "expenses.json"
CATEGORIES = ("Food", "Travel", "Shopping", "Bills", "Education", "Health", "Other")


def load_expenses():
    """Load saved expenses; return an empty list if no file exists yet."""
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read saved data. Starting with an empty list.")
        return []


def save_expenses(expenses):
    """Persist expenses as JSON."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4, ensure_ascii=False)


def read_amount(prompt="Enter amount (INR): "):
    while True:
        try:
            amount = float(input(prompt).strip())
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Please enter a valid number.")


def add_expense(expenses):
    title = input("Expense description: ").strip()
    if not title:
        print("Description cannot be empty.")
        return
    print("Categories:", ", ".join(CATEGORIES))
    category = input("Category: ").strip().title()
    if category not in CATEGORIES:
        print("Unknown category. Using 'Other'.")
        category = "Other"
    amount = read_amount()
    expense = {
        "id": max((item.get("id", 0) for item in expenses), default=0) + 1,
        "title": title,
        "category": category,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    expenses.append(expense)
    save_expenses(expenses)
    print("Expense saved successfully.")


def view_expenses(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return
    print("\n{:<4} {:<20} {:<14} {:>12}  {}".format(
        "ID", "Description", "Category", "Amount", "Date"))
    print("-" * 75)
    for item in expenses:
        print("{:<4} {:<20} {:<14} {:>12.2f}  {}".format(
            item["id"], item["title"][:20], item["category"],
            item["amount"], item["date"]))


def show_total(expenses):
    total = sum(item["amount"] for item in expenses)
    print(f"Total expenditure: INR {total:,.2f}")


def show_summary(expenses):
    if not expenses:
        print("No expenses available for summary.")
        return
    totals = {}
    for item in expenses:
        totals[item["category"]] = totals.get(item["category"], 0) + item["amount"]
    print("\nExpense summary by category")
    for category, amount in sorted(totals.items()):
        print(f"  {category:<14} INR {amount:,.2f}")
    highest = max(expenses, key=lambda item: item["amount"])
    lowest = min(expenses, key=lambda item: item["amount"])
    print(f"Highest expense: {highest['title']} (INR {highest['amount']:.2f})")
    print(f"Lowest expense:  {lowest['title']} (INR {lowest['amount']:.2f})")
    show_total(expenses)


def search_category(expenses):
    category = input("Enter category to search: ").strip().title()
    matches = [item for item in expenses if item["category"] == category]
    view_expenses(matches)
    if matches:
        print(f"Category total: INR {sum(x['amount'] for x in matches):,.2f}")


def main():
    expenses = load_expenses()
    actions = {
        "1": lambda: add_expense(expenses),
        "2": lambda: view_expenses(expenses),
        "3": lambda: show_total(expenses),
        "4": lambda: show_summary(expenses),
        "5": lambda: search_category(expenses),
    }
    while True:
        print("\n=== PERSONAL EXPENSE TRACKER ===")
        print("1. Add expense\n2. View expenses\n3. Total expenditure")
        print("4. Category summary\n5. Search by category\n6. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "6":
            print("Thank you for using Personal Expense Tracker.")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()
