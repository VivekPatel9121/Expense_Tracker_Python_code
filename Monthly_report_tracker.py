import json
import os
from datetime import datetime

FILE_NAME = "expenses.json"


def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)


def add_expense():
    expenses = load_expenses()

    print("\n===== Add New Expense =====")
    date = input("Enter date (YYYY-MM-DD): ").strip()
    category = input("Enter category (Food, Travel, Shopping, etc.): ").strip()
    description = input("Enter description: ").strip()
    amount_input = input("Enter amount: ").strip()

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.\n")
        return

    try:
        amount = float(amount_input)
        if amount <= 0:
            print("Amount must be greater than 0.\n")
            return
    except ValueError:
        print("Invalid amount.\n")
        return

    expense_id = 1
    if expenses:
        expense_id = max(expense["id"] for expense in expenses) + 1

    new_expense = {
        "id": expense_id,
        "date": date,
        "category": category,
        "description": description,
        "amount": amount
    }

    expenses.append(new_expense)
    save_expenses(expenses)
    print("Expense added successfully.\n")


def view_expenses():
    expenses = load_expenses()

    print("\n===== All Expenses =====")
    if not expenses:
        print("No expenses found.\n")
        return

    for expense in expenses:
        print(f"ID: {expense['id']}")
        print(f"Date: {expense['date']}")
        print(f"Category: {expense['category']}")
        print(f"Description: {expense['description']}")
        print(f"Amount: ₹{expense['amount']:.2f}")
        print("-" * 35)
    print()


def search_expense_by_category():
    expenses = load_expenses()

    print("\n===== Search Expense by Category =====")
    category = input("Enter category name: ").strip().lower()

    found = False
    total = 0

    for expense in expenses:
        if expense["category"].lower() == category:
            print(f"ID: {expense['id']} | Date: {expense['date']} | Description: {expense['description']} | Amount: ₹{expense['amount']:.2f}")
            total += expense["amount"]
            found = True

    if found:
        print(f"Total for category '{category}': ₹{total:.2f}\n")
    else:
        print("No expenses found in this category.\n")


def delete_expense():
    expenses = load_expenses()

    print("\n===== Delete Expense =====")
    expense_id_input = input("Enter expense ID to delete: ").strip()

    try:
        expense_id = int(expense_id_input)
    except ValueError:
        print("Invalid expense ID.\n")
        return

    for expense in expenses:
        if expense["id"] == expense_id:
            expenses.remove(expense)
            save_expenses(expenses)
            print("Expense deleted successfully.\n")
            return

    print("Expense ID not found.\n")


def monthly_report():
    expenses = load_expenses()

    print("\n===== Monthly Expense Report =====")
    month = input("Enter month (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Invalid month format. Please use YYYY-MM.\n")
        return

    monthly_expenses = []
    total_amount = 0
    category_totals = {}

    for expense in expenses:
        if expense["date"].startswith(month):
            monthly_expenses.append(expense)
            total_amount += expense["amount"]

            category = expense["category"]
            if category in category_totals:
                category_totals[category] += expense["amount"]
            else:
                category_totals[category] = expense["amount"]

    if not monthly_expenses:
        print("No expenses found for this month.\n")
        return

    print(f"\nExpenses for {month}:")
    for expense in monthly_expenses:
        print(f"ID: {expense['id']} | Date: {expense['date']} | Category: {expense['category']} | Description: {expense['description']} | Amount: ₹{expense['amount']:.2f}")

    print("\nCategory-wise Total:")
    for category, amount in category_totals.items():
        print(f"{category}: ₹{amount:.2f}")

    print(f"\nTotal Monthly Expense: ₹{total_amount:.2f}\n")


def menu():
    while True:
        print("===== Expense Tracker =====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Search Expense by Category")
        print("4. Delete Expense")
        print("5. Monthly Report")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            search_expense_by_category()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            monthly_report()
        elif choice == "6":
            print("Thank you for using Expense Tracker.")
            break
        else:
            print("Invalid choice. Please try again.\n")


menu()