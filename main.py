import json
import csv
import os
from datetime import date

jsonfile = 'expenses.json'
csvfile = 'expenses.csv'
base_path = os.path.dirname(os.path.abspath(__file__))
jsonfilepath = os.path.join(base_path, jsonfile)
csvfilepath = os.path.join(base_path, csvfile)


class Expense:
    def __init__(self, amount, category, description):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = str(date.today())  


class Tracker:
    def __init__(self):
        try:
            with open(jsonfilepath, "r") as f:
                self.data = json.load(f)
        except json.JSONDecodeError:
            print("File corrupt, resetting library")
            self.data = {"Expenses": []}
        except FileNotFoundError:
            self.data = {"Expenses": []}
            with open(jsonfilepath, 'w') as f:
                json.dump(self.data, f, indent=4)

    
    def _format_expense(self, expense):
        return (
            f"{'-' * 30}\n"
            f"Amount: {expense['amount']} Rs\n"
            f"Category: {expense['category']}\n"
            f"Description: {expense['description']}\n"
            f"Date: {expense['date']}\n"
            f"{'-' * 30}"
        )

    def add_expense(self, expense):
        exp = {
            'amount': expense.amount,
            'category': expense.category,
            'description': expense.description,
            'date': expense.date,
        }

        if exp in self.data['Expenses']:
            print("Expense already in expenses")
        else:
            self.data['Expenses'].append(exp)
            with open(jsonfilepath, 'w') as f:
                json.dump(self.data, f, indent=4)
            return True

    def view_expenses(self):
        if not self.data['Expenses']:
            print("You have no expenses")
        else:
            for expense in self.data['Expenses']:
                print(self._format_expense(expense))  # Fix 4: use helper

    def view_by_category(self, category):
        if self.data['Expenses']:
            
            matches = [e for e in self.data['Expenses'] if e['category'].lower() == category.lower()]
            if matches:
                for expense in matches:
                    print(self._format_expense(expense))  # Fix 4: use helper
            else:
                print(f"No expenses found for category '{category}'")
        else:
            print("You have no expenses")

    
    def view_by_date(self, start_date_str, end_date_str):
        if not self.data['Expenses']:
            print("You have no expenses")
            return

        try:
            start = date.fromisoformat(start_date_str)
            end = date.fromisoformat(end_date_str)
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        if start > end:
            print("Start date must be before or equal to end date.")
            return

        matches = [
            e for e in self.data['Expenses']
            if start <= date.fromisoformat(e['date']) <= end
        ]

        if matches:
            for expense in matches:
                print(self._format_expense(expense))  # Fix 4: use helper
        else:
            print(f"No expenses found between {start_date_str} and {end_date_str}")

    
    def export(self):
        try:
            with open(csvfilepath, 'w', newline='') as f:
                fieldnames = ['amount', 'category', 'description', 'date']
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
                writer.writeheader()
                writer.writerows(self.data['Expenses'])
            print(f"Exported successfully to '{csvfilepath}'.")
            print("Your JSON data has been kept intact. Delete it manually if you no longer need it.")
        except Exception as e:
            print(f"Export failed: {e}. Your data has NOT been deleted.")

    
    def view_summary(self):
        if not self.data['Expenses']:
            print("You have no expenses")
            return

        total = sum(e['amount'] for e in self.data['Expenses'])

        category_totals = {}
        for e in self.data['Expenses']:
            cat = e['category']
            category_totals[cat] = category_totals.get(cat, 0) + e['amount']

        highest = max(self.data['Expenses'], key=lambda x: x['amount'])

        print(f"\n{'=' * 30}")
        print(f"  EXPENSE SUMMARY")
        print(f"{'=' * 30}")
        print(f"Total spent: {total} Rs")
        print(f"\nSpending by category:")
        for cat, amt in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {amt} Rs")
        print(f"\nHighest single expense: {highest['amount']} Rs")
        print(f"  ({highest['description']} on {highest['date']})")
        print(f"{'=' * 30}\n")


def main():
    exp_tracker = Tracker()
    while True:
        print("\nEXPENSES TRACKER")
        print("1. Add expense\n2. View all expenses\n3. View by category\n4. View by date range\n5. Export to CSV\n6. Summary\n7. Exit")
        try:
            choice = int(input("Enter the number corresponding to the action you want to do: "))
        except ValueError:
            print("Invalid input, try again")
            continue

        if choice < 1 or choice > 7:
            print("Invalid input, try again")
            continue
        elif choice == 1:
            try:
                amount = int(input("Enter the amount for the expense: "))
            except ValueError:
                print("Please enter a number")
                continue
            category = input("Enter the category of the expense: ")
            des = input("Enter the description of the expense: ")
            exp = Expense(amount, category, des)
            exp_tracker.add_expense(exp)
            print("Expense added")
        elif choice == 2:
            exp_tracker.view_expenses()
        elif choice == 3:
            cat = input("Enter the category: ")
            exp_tracker.view_by_category(cat)
        elif choice == 4:
            
            d1 = input("Enter the start date (YYYY-MM-DD): ")
            d2 = input("Enter the end date (YYYY-MM-DD): ")
            exp_tracker.view_by_date(d1, d2)
        elif choice == 5:
            yn = input("Export expenses to CSV? The JSON data will NOT be deleted.\n(y/n): ")
            if yn.lower() == 'y':
                exp_tracker.export()
            elif yn.lower() == 'n':
                continue
            else:
                print("Invalid")
                continue
        elif choice == 6:
            exp_tracker.view_summary()
        elif choice == 7:
            print("Bye!")
            break


if __name__ == "__main__":
    main()
