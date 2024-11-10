# def example():
#     print("Start")
#     return
#     print("This is unreachable")

# def another_example():
#     for i in range(5):
#         if i > 2:
#             break
#         print(i)
#         continue
#         print("Also unreachable")

def simple_function():
    pass

def complex_function(x):
    if x > 0:
        for i in range(x):
            while i < 10:
                if i % 2 == 0:
                    print(i)
    else:
        try:
            with open("file.txt") as f:
                data = f.read()
        except Exception as e:
            print("Error")

def another_function(y):
    return y and (y > 0 or y < 10)