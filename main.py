"""
Expense Tracker Application

This module provides a simple expense tracking application that allows users to:
- Add new expenses with details such as amount, category, description, and date.
- View all expenses or filter them by category.
- View a summary of expenses with a breakdown by category.
- Filter expenses and summaries by time (day, week, month, year).

The application loads and saves expenses to a text file (`expenses.txt`), ensuring that data is preserved
between sessions. If the file does not exist, it is created with the appropriate headers.

Functions:
    main_menu: Displays the main menu and handles user interactions.
    add_expense: Prompts the user to add a new expense.
    add_new_category: Prompts the user to add a new category for expenses.
    convert_str_to_date: Converts a string representing a date into a `date` object.
    confirm: Prompts the user for a confirmation (yes/no).
    append_expense_to_file: Appends a new expense to the `expenses.txt` file.
    view_expenses: Allows the user to view or filter expenses.
    display_category: Displays the list of expenses in a tabular format.
    filter_category: Filters expenses by category.
    view_summary: Allows the user to view a summary of expenses.
    display_summary: Displays the summary of total expenses and category breakdown.
    filter_summary_by_time: Filters the expense summary based on time (day, week, month, year).
    main: Initializes the expense tracker, loads data, and starts the main menu.
"""

from datetime import datetime, timedelta, date
from typing import Union, Optional


def main_menu(expenses: list[dict[str, Union[int, str, date]]], categories: list[str]) -> None:
    """
    Displays the main menu and handles user interactions for selecting actions.

    Args:
        expenses (list[dict[str, Union[int, str, date]]]):
            A list of expense dictionaries, where each dictionary contains details such as
            amount (int), category (str), description (str), and date (date).
        categories (list[str]): A list of expense categories.
    """

    is_running = True
    while is_running:
        print("""
--------------------------------------------------
    Expense Tracker
    1) Add Expense
    2) View Expenses
    3) View Summary
    4) Exit
--------------------------------------------------""")

        selection = input("Please select the action you would like to perform: ")
        match selection.lower():
            case "1":
                add_expense(expenses, categories)
            case "2":
                display_category(expenses)
                view_expenses(expenses, categories)
            case "3":
                display_summary(expenses)
                view_summary(expenses)
            case "4":
                print("Exiting system...")
                is_running = False
            case _:
                print("Please enter a valid selection!")


def add_expense(expenses: list[dict[str, Union[int, str, date]]], categories: list[str]) -> None:
    """
    Allows the user to add a new expense to the tracker.

    Args:
        expenses (list[dict[str, Union[int, str, date]]]):
            A list of expense dictionaries, where each dictionary contains details such as
            amount (int), category (str), description (str), and date (date).
        categories (list[str]): A list of expense categories.
    """

    temp: dict[str, Union[int, str, date]] = {}

    while True:
        amount = input("Please enter the amount of the expense: ")

        if amount.isdecimal() and int(amount) >= 0:
            temp["amount"] = int(amount)
            break

        print("Please enter a valid amount!")

    while not categories:
        add_new_category(categories)

    while True:
        print(f"Categories: {categories}")
        category = input("Please select the category for the expense (type 'new' to add new category): ").title()

        if category == "New":
            add_new_category(categories)
            continue

        if category in categories:
            temp["category"] = category
            break

        print("Please enter a valid selection!")

    while True:
        description = input("Please enter a description for the expense: ")

        if description:
            temp["description"] = description
            break

        print("Please enter a valid description!")

    while True:
        expense_date = convert_str_to_date(input("Please enter the date of the expense (YYYY-MM-DD): "))

        if expense_date:
            temp["date"] = expense_date
            break

        print("Please enter a valid date according to the format given!")

    if confirm(temp, "Are you sure you would like to append the expense above (y/n): "):
        expenses.append(temp)
        append_expense_to_file(temp)


def add_new_category(categories: list[str]) -> None:
    """
    Allows the user to add a new category to the tracker.

    Args:
        categories (list[str]): A list of expense categories.
    """

    while True:
        new_category = input("Please enter the name for the new category: ").title()

        if all(i.isalpha() or i.isspace() for i in new_category):
            confirmation = confirm(
                {"New Category": new_category},
                "Are you sure you would like to add the category above (y/n): "
            )

            if confirmation:
                categories.append(new_category)
                print(f"{new_category} is added as a new category")

            break

        print("Please enter a valid category name!")


def convert_str_to_date(expense_date: str) -> Optional[date]:
    """
    Converts a string representation of a date to a `date` object.

    Args:
        expense_date (str): A string representing the date in YYYY-MM-DD format.

    Returns:
        Optional[date]: A `date` object if the conversion is successful, otherwise `None`.
    """

    try:
        return datetime.strptime(expense_date, "%Y-%m-%d").date()
    except ValueError:
        return


def confirm(inputs: dict[str, Union[int, str, date]], prompt: str) -> bool:
    """
    Prompts the user for confirmation based on the provided inputs.

    Args:
        inputs (dict[str, Union[int, str, date]]): A dictionary of values to display for confirmation.
        prompt (str): A prompt string to ask for confirmation.

    Returns:
        bool: `True` if the user confirms, otherwise `False`.
    """

    while True:
        for key, value in inputs.items():
            print(f"{key} : {value}")
        selection = input(prompt).lower()

        if selection == "y":
            return True
        elif selection == "n":
            return False
        else:
            print("Please enter a valid selection!")


def append_expense_to_file(expense: dict[str, Union[int, str, date]]) -> None:
    """
    Appends a new expense to the expenses file.

    Args:
        expense (list[dict[str, Union[int, str, date]]]):
            A expense dictionary, where each dictionary contains details such as
            amount (int), category (str), description (str), and date (date).
    """

    line = ",".join(str(value) for value in expense.values()) + "\n"

    with open("expenses.txt", "a") as expenses_file:
        expenses_file.write(line)


def view_expenses(expenses: list[dict[str, Union[int, str, date]]], categories: list[str]) -> None:
    """
    Displays options to view or filter expenses.

    Args:
        expenses (list[dict[str, Union[int, str, date]]]):
            A list of expense dictionaries, where each dictionary contains details such as
            amount (int), category (str), description (str), and date (date).
        categories (list[str]): A list of expense categories.
    """

    while True:
        print("""
--------------------------------------------------
    View Expenses
    1) Display All Expenses
    2) Filter Expenses By Category
    3) Return To Main Menu
--------------------------------------------------""")
        selection = input("Please enter the action you would like to perform: ")

        match selection:
            case "1":
                display_category(expenses)
            case "2":
                filter_category(expenses, categories)
            case "3":
                break
            case _:
                print("Please enter a valid selection!")


def display_category(expenses: list[dict[str, Union[int, str, date]]]) -> None:
    """
    Displays expenses in a tabular format.

    Args:
        expenses (list[dict[str, Union[int, str, date]]]):
            A list of expense dictionaries, where each dictionary contains details such as
            amount (int), category (str), description (str), and date (date).
    """

    print("""
--------------------------------------------------
Amount    Category       Description    Date
--------------------------------------------------""")

    for expense in expenses:
        print(f"{expense['amount']:<10}"
              f"{expense['category']:<15}"
              f"{expense['description']:<15}"
              f"{str(expense['date']):<15}")

    print("--------------------------------------------------")


def filter_category(expenses: list[dict[str, Union[int, str, date]]], categories: list[str]) -> None:
    """
    Filters and displays expenses by the selected category.

    Args:
        expenses (list[dict[str, Union[int, str, date]]]):
            A list of expense dictionaries, where each dictionary contains details such as
            amount (int), category (str), description (str), and date (date).
        categories (list[str]): A list of expense categories.
    """

    while True:
        print(f"Categories: {categories}")
        category = input("Please select the category that you would like to filter by: ").title()

        if category in categories:
            filtered_expenses = [expense for expense in expenses if expense["category"] == category]
            break

        print("Please enter a valid selection!")

    display_category(filtered_expenses)


def view_summary(expenses: list[dict[str, Union[int, str, date]]]) -> None:
    """
    Displays options to view a summary of expenses.

    Args:
        expenses (list[dict[str, Union[int, str, date]]]):
            A list of expense dictionaries, where each dictionary contains details such as
            amount (int), category (str), description (str), and date (date).
    """

    while True:
        print("""
--------------------------------------------------
    View Summary
    1) Display Summary
    2) Filter Summary By Time
    3) Return To Main Menu
--------------------------------------------------""")
        selection = input("Please enter the action you would like to perform: ")

        match selection:
            case "1":
                display_summary(expenses)
            case "2":
                filter_summary_by_time(expenses)
            case "3":
                break
            case _:
                print("Please enter a valid selection!")


def display_summary(expenses: list[dict[str, Union[int, str, date]]], filter_output_str: str = "") -> None:
    """
    Displays a summary of the expenses, including the total amount and a category-wise breakdown.

    Args:
        expenses (list[dict[str, Union[int, str, date]]]):
            A list of expense dictionaries, where each dictionary contains details such as
            amount (int), category (str), description (str), and date (date).
        filter_output_str (str, optional):
            An optional string to specify additional information about the filter
            applied (e.g., "Of Current Month").
    """

    total = sum(expense["amount"] for expense in expenses)

    print(f"""
--------------------------------------------------
    Total Expenses{filter_output_str}: {total}
    Category Breakdown:""")

    category_expenses = {}

    for expense in expenses:
        if expense["category"] not in category_expenses:
            category_expenses[expense["category"]] = expense["amount"]
        else:
            category_expenses[expense["category"]] += expense["amount"]

    for key, value in category_expenses.items():
        print(f"        - {key} : {value}")

    print("--------------------------------------------------")


def filter_summary_by_time(expenses: list[dict[str, Union[int, str, date]]]) -> None:
    """
    Filters the summary of expenses based on a specified time period (day, week, month, or year).

    Args:
        expenses (list[dict[str, Union[int, str, date]]]):
            A list of expense dictionaries, where each dictionary contains details such as
            amount (int), category (str), description (str), and date (date).
    """

    while True:
        time_filter = ["Day", "Week", "Month", "Year"]

        print(f"Time filter: {time_filter}")
        selection = input("Please select a time filter that you would like to filter by: ").lower()

        today = datetime.now().date()
        match selection:
            case "day":
                filtered_expenses = [expense for expense in expenses if expense["date"] == today]
                break
            case "week":
                start_of_week = today - timedelta(days=today.weekday())
                end_of_week = start_of_week + timedelta(days=6)
                filtered_expenses = [expense for expense in expenses if
                                     start_of_week <= expense["date"] <= end_of_week]
                break
            case "month":
                filtered_expenses = [expense for expense in expenses if
                                     expense["date"].year == today.year and expense["date"].month == today.month]
                break
            case "year":
                filtered_expenses = [expense for expense in expenses if expense["date"].year == today.year]
                break
            case _:
                print("Please select a valid filter!")

    display_summary(filtered_expenses, f" Of Current {selection.title()}")


def main() -> None:
    """
    Main function that initializes the expense tracker application.
    Loads existing data from the expenses file or creates a new one if not found.
    Launches the main menu for user interaction.
    """

    expenses: list[dict[str, Union[int, str, date]]] = []

    print("Loading data...")
    try:
        with (open("expenses.txt", "r") as expenses_file):
            expenses_file.readline()

            for line in expenses_file:
                line = line.split(",")

                amount = int(line[0])
                category = line[1]
                description = line[2]
                expense_date = datetime.strptime(line[3].removesuffix("\n"), "%Y-%m-%d").date()

                expenses.append({
                    "amount": amount,
                    "category": category,
                    "description": description,
                    "date": expense_date
                })

    except FileNotFoundError:
        with open("expenses.txt", "w") as expenses_file:
            expenses_file.write("amount,category,description,date\n")
            expenses_file.close()

    categories: list[str] = list({expense["category"] for expense in expenses})
    main_menu(expenses, categories)


if __name__ == '__main__':
    main()
