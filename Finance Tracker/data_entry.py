from datetime import datetime

CATEGORIES = {"I":"Income", "E":"Expense"}
def get_date(prompt, allow_default = False):
    date = input(prompt)
    if allow_default and not date:
        return datetime.today().strftime("%d-%m-%Y")
    
    try:
        validate_date = datetime.strptime(date, "%d-%m-%Y")
        return validate_date.strftime("%d-%m-%Y")
    except ValueError:
        print("Date format is invalid. Please enter date in dd-mm-yyy")
        return get_date(prompt, allow_default)

def get_amount():
    try:
        amount = float(input("Enter the amount (without Rs): "))
        if amount < 0:
            raise ValueError("Amount must be greater than zero")
        return amount
    except ValueError:
        print(ValueError)
        return get_amount()

def get_category():
    category = input("Enter the category ('I' for income and 'E' for expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    
    print("Invalid category")
    return get_category()

def get_description():
    return input("Enter description (optional): ")

