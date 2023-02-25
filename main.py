import tkinter as tk
from tkinter import messagebox


# Simple budget tracker which calculates income and expenses
class BudgetTracker:
    def __init__(self):
        self.balance = 0
        self.income = []
        self.expenses = []

    def add_income(self, source, amount):
        self.income.append((source, amount))
        self.balance = self.get_total_income() - self.get_total_expense()

    def add_expense(self, expense_source, expense_amount):
        self.expenses.append((expense_source, expense_amount))
        self.balance -= expense_amount

    def undo_add_income(self):
        if self.income:
            last_income_source, last_amount = self.income.pop()
            self.balance = self.get_total_income() - self.get_total_expense()
            return last_income_source, last_amount
        else:
            return None, None

    def undo_add_expense(self):
        if self.expenses:
            last_expense_source, last_expense_amount = self.expenses.pop()
            self.balance = self.get_total_income() - self.get_total_expense()
            return last_expense_source, last_expense_amount
        else:
            return None, None

    def get_balance(self):
        return self.balance

    def get_total_income(self):
        return sum(amount[1] for amount in self.income)

    def get_total_expense(self):
        return sum(expense[1] for expense in self.expenses)


# Initialize GUI
root = tk.Tk()
root.title("Budget Tracker")
root.config(bg="light blue")  # Set background colour
root.geometry('500x800')  # Set size

# Initialize Budget Tracker
budget_tracker = BudgetTracker()

# Expense type label
frequency_label = tk.Label(root, text="Select Income Frequency:", bg="light blue", highlightbackground="light blue")
frequency_label.grid(row=0, column=1, sticky="W")

# Income frequency dropdown set as weekly
income_frequency_var = tk.StringVar()
income_frequency_var.set("Weekly")

# Select if weekly or monthly (this doesn't do anything)
income_frequency_menu = tk.OptionMenu(root, income_frequency_var, "Weekly", "Monthly")
income_frequency_menu.grid(row=0, column=2, sticky="W")
income_frequency_menu.config(bg="light blue")


# Option to add income, includes error message if number is not added into amount entry
def add_income_button_click():
    try:
        income = float(income_entry.get())
    except ValueError:
        tk.messagebox.showerror("Error", "Please enter a valid number in the income amount field.")
        return

    income_source = income_source_entry.get()
    budget_tracker.add_income(income_source, income)
    income_display_label.config(text=f"{income_source}: {income} \n{income_display_label['text']}")
    balance_label.config(text=f"Current balance: {budget_tracker.get_balance()}")
    total_income_label.config(text=f"Total Income: {budget_tracker.get_total_income()}")
    income_entry.delete(0, 'end')
    income_source_entry.delete(0, 'end')


# Option tp undo last added income, can keep undoing
def undo_add_income_button_click():
    last_income_source, last_amount = budget_tracker.undo_add_income()
    if last_income_source:
        # Find the index of the last line containing the source and amount
        index = income_display_label['text'].find(f"{last_income_source}: {last_amount}")
        if index != -1:
            # Get the text before and after the line, and concatenate them
            text_before = income_display_label['text'][:index].rstrip('\n')
            text_after = income_display_label['text'][index:].split('\n', 1)[1]
            income_display_label.config(text=f"{text_after}\n{text_before}")
        balance_label.config(text=f"Current balance: {budget_tracker.get_balance()}")
        total_income_label.config(text=f"Total Income: {budget_tracker.get_total_income()}")
    income_entry.delete(0, 'end')
    income_source_entry.delete(0, 'end')


# Set frame parameter
frame = tk.Frame(root)
frame.grid(row=7, column=1)
frame.grid_propagate(False)
frame.config(width=150, height=200)

# Income amount label
income_label = tk.Label(root, text="Income Amount:", bg="light blue")
income_label.grid(row=1, column=1, sticky="W")

# Income amount entry box
income_entry = tk.Entry(root, highlightbackground="light blue")
income_entry.grid(row=2, column=1, sticky="W")

# Income type label
income_source_label = tk.Label(root, text="Income Source:", bg="light blue", highlightbackground="light blue")
income_source_label.grid(row=3, column=1, sticky="W")

# Income type entry box
income_source_entry = tk.Entry(root, highlightbackground="light blue")
income_source_entry.grid(row=4, column=1)

# Add income button
add_income_button = tk.Button(root, text="Add Income", command=add_income_button_click,
                              highlightbackground="light blue", bg="light blue")
add_income_button.grid(row=5, column=1)

# Undo add expenses button
undo_add_income_button = tk.Button(root, text="Undo", command=undo_add_income_button_click,
                                   highlightbackground="light blue")
undo_add_income_button.grid(row=6, column=1)


# Display incomes
income_display_label = tk.Label(frame, text="", anchor="w", justify=tk.LEFT)
income_display_label.grid(row=0, column=0, sticky="nw")


total_income_label = tk.Label(root, text="Total Income: 0", bg="light blue")
total_income_label.grid(row=8, column=1)


frame.columnconfigure(0, minsize=200)
frame.rowconfigure(0, minsize=200)


# Add buttons to add and stop adding expenses, includes error message if number not entered in amount
def add_expense_button_click():
    try:
        expense = float(expense_entry.get())
    except ValueError:
        tk.messagebox.showerror("Error", "Please enter a valid number in the expense amount field.")
        return

    expense_source = expense_source_entry.get()
    budget_tracker.add_expense(expense_source, expense)
    expense_display_label.config(text=f"{expense_source}: {expense} \n{expense_display_label['text']}")
    balance_label.config(text=f"Current balance: {budget_tracker.get_balance()}")
    total_expenses_label.config(text=f"Total Expenses: {budget_tracker.get_total_expense()}")
    expense_entry.delete(0, 'end')
    expense_source_entry.delete(0, 'end')


# Undo function (same as income)
def undo_add_expense_button_click():
    last_expense_source, last_expense_amount = budget_tracker.undo_add_expense()
    if last_expense_source:
        # Find index of last line containing source and amount
        index = expense_display_label['text'].find(f"{last_expense_source}: {last_expense_amount}")
        if index != -1:
            # Get text before and after line and concatenate
            text_before = expense_display_label['text'][:index].rstrip('\n')
            text_after = expense_display_label['text'][index:].split('\n', 1)[1]
            expense_display_label.config(text=f"{text_after}\n{text_before}")
        balance_label.config(text=f"Current balance: {budget_tracker.get_balance()}")
        total_expenses_label.config(text=f"Total Expenses: {budget_tracker.get_total_expense()}")
    expense_entry.delete(0, 'end')
    expense_source_entry.delete(0, 'end')


# Set frame parameter
frame = tk.Frame(root)
frame.grid(row=7, column=2)
frame.grid_propagate(False)
frame.config(width=150, height=200)

# Expense amount label
expense_label = tk.Label(root, text="Expense Amount:", bg="light blue")
expense_label.grid(row=1, column=2, sticky="W")

# Expense amount entry box
expense_entry = tk.Entry(root, highlightbackground="light blue")
expense_entry.grid(row=2, column=2, sticky="W")

# Expense type label
expense_source_label = tk.Label(root, text="Expense Type:", bg="light blue", highlightbackground="light blue")
expense_source_label.grid(row=3, column=2, sticky="W")

# Expense type entry box
expense_source_entry = tk.Entry(root, highlightbackground="light blue")
expense_source_entry.grid(row=4, column=2)

# Add expenses button
add_expense_button = tk.Button(root, text="Add Expense", command=add_expense_button_click, highlightbackground="light blue")
add_expense_button.grid(row=5, column=2)

# Undo add expenses button
undo_add_expense_button = tk.Button(root, text="Undo", command=undo_add_expense_button_click, highlightbackground="light blue")
undo_add_expense_button.grid(row=6, column=2)

# Display expenses
expense_display_label = tk.Label(frame, text="", anchor="w", justify=tk.LEFT)
expense_display_label.grid(row=0, column=2, sticky="nw")

# Total expenses
total_expenses_label = tk.Label(root, text="Total Expenses: 0", bg="light blue")
total_expenses_label.grid(row=8, column=2)


# Add a label to display the balance
balance_label = tk.Label(root, text="Current balance: 0", bg="light blue")
balance_label.grid(row=9, column=1)


root.mainloop()
