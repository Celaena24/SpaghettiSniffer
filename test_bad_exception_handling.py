def example_function():
    try:
        x = 1 / 0
    except:
        print("Caught an exception")
    
    try:
        y = 1 / 0
    except ZeroDivisionError:
        print("Caught division by zero")

    try:
        z = int("not a number")
    except ValueError:
        print("Caught value error")

    try:
        w = [1, 2, 3]
        print(w[5])
    except:
        print("Caught another exception")