import matplotlib.pyplot as plt  
import pandas as pd  
import csv
from datetime import datetime
from data_entry import get_category, get_amount, get_date, get_description

class CSV:
    csv_file = "data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    DATE_FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.csv_file)
        except FileNotFoundError:
            print("CSV file not found, Creating one...")
            data_frame = pd.DataFrame(columns=cls.COLUMNS)
            data_frame.to_csv(cls.csv_file, index=False)

    @classmethod
    def add_data(cls, date, amount, category, description):
        new_data = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.csv_file, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=cls.COLUMNS)
            writer.writerow(new_data)
        print("Data added successfully!")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        dataframe = pd.read_csv(cls.csv_file)

        # Convert `date` column to DateTime format
        dataframe["date"] = pd.to_datetime(dataframe["date"], format=cls.DATE_FORMAT)
        dataframe["amount"] = dataframe["amount"].astype(float)  # Convert amount to float

        start_date = datetime.strptime(start_date, cls.DATE_FORMAT)
        end_date = datetime.strptime(end_date, cls.DATE_FORMAT)

        # Mask for filtering transactions
        mask = (start_date <= dataframe["date"]) & (end_date >= dataframe["date"])
        filtered_dataframe = dataframe.loc[mask]

        if filtered_dataframe.empty:
            print("No transactions found within the specified date range.")
        else:
            print(f"-------- Transactions from {start_date.strftime(cls.DATE_FORMAT)} to {end_date.strftime(cls.DATE_FORMAT)} --------")
            print(filtered_dataframe.to_string(index=False, formatters={"date": lambda x: x.strftime(cls.DATE_FORMAT)}))

            total_income = filtered_dataframe[filtered_dataframe["category"] == "Income"]["amount"].sum()
            total_expense = filtered_dataframe[filtered_dataframe["category"] == "Expense"]["amount"].sum()

            print("\n Summary:")
            print(f"Total Income: Rs. {total_income:.2f}")
            print(f"Total Expense: Rs. {total_expense:.2f}")
            print(f"Net Savings: Rs. {(total_income - total_expense):.2f}")

            return filtered_dataframe

def add():
    CSV.initialize_csv()
    date = get_date("Enter the date (dd-mm-yyyy) [Press 'Enter' if the date is today]: ", True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_data(date, amount, category, description)

def plot_transactions(dataframe):
    if dataframe.empty:
        print("No data available to plot.")
        return

    dataframe.set_index("date", inplace=True)
    dataframe.index = pd.to_datetime(dataframe.index, format="%d-%m-%Y")

    income_dataframe = dataframe[dataframe["category"] == "Income"].resample("D").sum().reindex(dataframe.index, fill_value=0)
    expense_dataframe = dataframe[dataframe["category"] == "Expense"].resample("D").sum().reindex(dataframe.index, fill_value=0)

    plt.figure(figsize=(10, 6))
    plt.plot(income_dataframe.index, income_dataframe["amount"], label="Income", marker="o", linestyle="-", color="green")
    plt.plot(expense_dataframe.index, expense_dataframe["amount"], label="Expense", marker="o", linestyle="-", color="red")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income vs Expense Over Time")
    plt.legend()
    plt.grid()
    plt.show()

def main():
    while True:
        print("\n--------- Welcome! ---------")
        print("01. Add Income or Expense")
        print("02. View Net Savings")
        print("03. Exit")
        print("--------------------------")
        choice = input("\nYour option: ")

        match choice:
            case '1' | '01':
                add()
            case '2' | '02':
                start_date = get_date("Enter the start date (dd-mm-yyyy): ")
                end_date = get_date("Enter the end date (dd-mm-yyyy): ")
                dataframe = CSV.get_transactions(start_date, end_date)

                if dataframe is not None and not dataframe.empty:
                    choice = input("\nDo you want to see it in a graph? ('Y' for yes, 'N' for no): ").strip().upper()
                    if choice == "Y":
                        print("Plotting Graph....")
                        plot_transactions(dataframe)
                    elif choice == "N":
                        print("Okay!")
                    else:
                        print("Invalid input. Enter 'Y' or 'N'!")
            case '3' | '03':
                print("Thank you!")
                break
            case _:
                print("Invalid Input. Try Again! \n")

if __name__ == "__main__":
    main()
