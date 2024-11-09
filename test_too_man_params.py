def too_many_params(a, b, c, d, e, f):
    pass

def another_too_many_params(a, b, c, d, e, f, g):
    pass

def just_enough_params(a, b, c, d, e):
    pass

def less_params(a, b, c, d):
    pass

def main():
    x = 10
    y = 15
    print(x+y)

    too_many_params(1, 2, 3, 4, 5, 6)
    another_too_many_params(1, 2, 3, 4, 5, 6, 7)
    just_enough_params(1, 2, 3, 4, 5)
    less_params(1, 2, 3, 4)

if __name__=="__main__":
    main()
