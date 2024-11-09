def example():
    print("Start")
    return
    print("This is unreachable")

def another_example():
    for i in range(5):
        if i > 2:
            break
        print(i)
        continue
        print("Also unreachable")

