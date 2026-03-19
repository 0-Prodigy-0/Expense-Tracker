#  Python Expense Tracker

A terminal-based expense tracking app built in Python. Log your expenses, filter them by category or date, view summaries, and export to CSV — all stored locally in a JSON file.

---

##  Project Structure

```
├── tracker.py        # Main application file
├── expenses.json     # Auto-created expense store
└── expenses.csv      # Generated on export
```

---

##  Getting Started

### Prerequisites

- Python 3.x (no third-party packages required)

### Running the App

```bash
python tracker.py
```

`expenses.json` is created automatically in the same directory on first run.

---

##  Menu Options

```
EXPENSES TRACKER
1. Add expense
2. View all expenses
3. View by category
4. View by date range
5. Export to CSV
6. Summary
7. Exit
```

---

##  Features

### 1. Add Expense
Enter an amount (integer, in Rs), a category, and a description. The current date is recorded automatically. Duplicate entries are rejected.

### 2. View All Expenses
Prints every stored expense in a formatted block:
```
------------------------------
Amount: 1700 Rs
Category: food
Description: radisson lunch
Date: 2026-03-19
------------------------------
```

### 3. View by Category
Filter expenses by category name (case-insensitive). Example: `food`, `Food`, and `FOOD` all match.

### 4. View by Date Range
Enter a start and end date in `YYYY-MM-DD` format to view expenses within that range (inclusive).

### 5. Export to CSV
Exports all expenses to `expenses.csv` as a tab-separated file. The JSON file is **not** deleted.

Example output:
```tsv
amount  category        description     date
1700    food            radisson lunch  2026-03-19
32000   entertainment   buying a ps5    2026-03-19
```

### 6. Summary
Displays:
- Total amount spent
- Spending broken down by category (highest first)
- Highest single expense

Example:
```
==============================
  EXPENSE SUMMARY
==============================
Total spent: 33700 Rs

Spending by category:
  entertainment: 32000 Rs
  food: 1700 Rs

Highest single expense: 32000 Rs
  (buying a ps5 on 2026-03-19)
==============================
```

---

##  Data Format (`expenses.json`)

```json
{
    "Expenses": [
        {
            "amount": 1700,
            "category": "food",
            "description": "radisson lunch",
            "date": "2026-03-19"
        }
    ]
}
```

The file is created automatically. Do not edit it manually unless you know what you're doing — a corrupt file will be reset and all data will be lost.

