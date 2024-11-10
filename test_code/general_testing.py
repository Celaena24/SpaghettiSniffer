# Sample code with bad coding practices for testing

import os  # Unused import, bad practice

def process_transactions(transactions):
    total_sum = 0
    index = 0
    while index < len(transactions):
        trans = transactions[index]
        if trans['amount'] < 0:
            print("Negative transaction ignored")  # Print statements instead of proper logging
            index += 1
            continue
        total_sum += trans['amount']
        if total_sum > 1000:
            print("Warning: Total sum exceeded 1000")  # Print statement
            total_sum -= 100  # Arbitrary adjustment, potential magic number
        index += 1
    print("Total transactions processed")  # Print statement
    return total_sum


# Function with high cyclomatic complexity and magic numbers
def calculate(things):
    result = []
    for item in things:
        if item > 10:
            result.append(item * 2)
            print("Large item processed")
        else:
            result.append(item - 2)
            print("Small item processed")
    result.sort()  # Modifies result in place, unclear why
    print("Calculation complete")
    return result


# A function with deep nesting, redundant checks, and non-specific exception handling
def check_and_log(data):
    if data:
        if isinstance(data, list):
            for i in range(len(data)):
                if data[i] != "error":
                    if len(data[i]) > 5:
                        try:
                            print(f"Data entry {i} is valid: {data[i]}")
                        except:
                            print("An unexpected error occurred")  # Non-specific exception handling
                    else:
                        if data[i].startswith("warn"):
                            print(f"Data entry {i} is a warning: {data[i]}")
                        else:
                            print("Invalid entry length")
                else:
                    print(f"Data entry {i} is an error")
        else:
            print("Data is not a list")
    else:
        print("No data provided")


# Function with too many parameters and direct comparison to True/False
def complex_function(a, b, c, d, e, f, g):
    if a == True:  # Direct comparison with True
        print("Parameter a is true")
    if b == False:  # Direct comparison with False
        print("Parameter b is false")
    # Dead code
    unused_var = 42
    for _ in range(5):
        pass

if __name__ == "__main__":
    transactions = [{"amount": 150}, {"amount": -50}, {"amount": 1000}, {"amount": 200}]
    process_transactions(transactions)

    things = [5, 12, 7, 25, 3]
    calculate(things)

    data = ["info123", "error", "warn56", "valid789"]
    check_and_log(data)

    complex_function(True, False, 1, 2, 3, 4, 5)
