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
        self.category = category.strip().lower()
        self.description = description.strip()
        self.date = str(date.today())


class Tracker:
    def __init__(self):
        try:
            with open(jsonfilepath, "r") as f:
                self.data = json.load(f)
        except json.JSONDecodeError:
            print("File corrupt, resetting data.")
            self.data = {"Expenses": []}
            self._save()
        except FileNotFoundError:
            self.data = {"Expenses": []}
            self._save()

    def _save(self):
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

        # Duplicate check: case-insensitive and stripped comparison
        for existing in self.data['Expenses']:
            if (
                existing['amount'] == exp['amount'] and
                existing['category'].lower() == exp['category'].lower() and
                existing['description'].lower().strip() == exp['description'].lower().strip() and
                existing['date'] == exp['date']
            ):
                print("This expense already exists.")
                return False

        self.data['Expenses'].append(exp)
        self._save()
        return True

    def delete_expense(self):
        if not self.data['Expenses']:
            print("You have no expenses to delete.")
            return

        for i, expense in enumerate(self.data['Expenses'], 1):
            print(f"{i}. {expense['description']} | {expense['amount']} Rs | {expense['category']} | {expense['date']}")

        while True:
            try:
                choice = int(input("Enter the number of the expense to delete (0 to cancel): "))
                if choice == 0:
                    return
                if 1 <= choice <= len(self.data['Expenses']):
                    removed = self.data['Expenses'].pop(choice - 1)
                    self._save()
                    print(f"Deleted: {removed['description']} ({removed['amount']} Rs)")
                    return
                else:
                    print(f"Please enter a number between 1 and {len(self.data['Expenses'])}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def edit_expense(self):
        if not self.data['Expenses']:
            print("You have no expenses to edit.")
            return

        for i, expense in enumerate(self.data['Expenses'], 1):
            print(f"{i}. {expense['description']} | {expense['amount']} Rs | {expense['category']} | {expense['date']}")

        while True:
            try:
                choice = int(input("Enter the number of the expense to edit (0 to cancel): "))
                if choice == 0:
                    return
                if 1 <= choice <= len(self.data['Expenses']):
                    exp = self.data['Expenses'][choice - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(self.data['Expenses'])}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        print("Leave a field blank to keep the current value.")

        new_amount = input(f"Amount [{exp['amount']}]: ").strip()
        if new_amount:
            while True:
                try:
                    exp['amount'] = float(new_amount)
                    if exp['amount'] <= 0:
                        raise ValueError
                    break
                except ValueError:
                    new_amount = input("Invalid. Enter a positive number for amount: ").strip()

        new_category = input(f"Category [{exp['category']}]: ").strip()
        if new_category:
            exp['category'] = new_category.lower()

        new_description = input(f"Description [{exp['description']}]: ").strip()
        if new_description:
            exp['description'] = new_description

        self._save()
        print("Expense updated successfully.")

    def view_expenses(self):
        if not self.data['Expenses']:
            print("You have no expenses.")
        else:
            for expense in self.data['Expenses']:
                print(self._format_expense(expense))

    def view_by_category(self, category):
        if not self.data['Expenses']:
            print("You have no expenses.")
            return

        matches = [e for e in self.data['Expenses'] if e['category'].lower() == category.lower().strip()]
        if matches:
            for expense in matches:
                print(self._format_expense(expense))
        else:
            print(f"No expenses found for category '{category}'.")

    def view_by_date(self, start_date_str, end_date_str):
        if not self.data['Expenses']:
            print("You have no expenses.")
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
                print(self._format_expense(expense))
        else:
            print(f"No expenses found between {start_date_str} and {end_date_str}.")

    def export(self):
        try:
            with open(csvfilepath, 'w', newline='') as f:
                fieldnames = ['amount', 'category', 'description', 'date']
                writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
                writer.writeheader()
                writer.writerows(self.data['Expenses'])
            print(f"Exported successfully to '{csvfilepath}'.")
            print("Your JSON data has been kept intact.")
        except Exception as e:
            print(f"Export failed: {e}. Your data has NOT been deleted.")

    def view_summary(self):
        if not self.data['Expenses']:
            print("You have no expenses.")
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
        print("1. Add expense")
        print("2. View all expenses")
        print("3. View by category")
        print("4. View by date range")
        print("5. Export to CSV")
        print("6. Summary")
        print("7. Edit expense")
        print("8. Delete expense")
        print("9. Exit")

        try:
            choice = int(input("Enter the number corresponding to the action: "))
        except ValueError:
            print("Invalid input, try again.")
            continue

        if choice < 1 or choice > 9:
            print("Invalid input, try again.")
            continue

        elif choice == 1:
            while True:
                try:
                    amount = float(input("Enter the amount for the expense: "))
                    if amount <= 0:
                        raise ValueError
                    break
                except ValueError:
                    print("Please enter a valid positive number.")
            category = input("Enter the category of the expense: ")
            des = input("Enter the description of the expense: ")
            exp = Expense(amount, category, des)
            if exp_tracker.add_expense(exp):
                print("Expense added successfully.")

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
            while True:
                yn = input("Export expenses to CSV? The JSON data will NOT be deleted. (y/n): ").strip().lower()
                if yn == 'y':
                    exp_tracker.export()
                    break
                elif yn == 'n':
                    break
                else:
                    print("Please enter y or n.")

        elif choice == 6:
            exp_tracker.view_summary()

        elif choice == 7:
            exp_tracker.edit_expense()

        elif choice == 8:
            exp_tracker.delete_expense()

        elif choice == 9:
            print("Bye!")
            break


if __name__ == "__main__":
    main()
