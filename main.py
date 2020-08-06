import timeit


# from meta import main

def print_file(python_file):
    f = open(python_file, 'r')
    for code in f:
        if code is not "\n":
            print(code)
    return


if __name__ == '__main__':
    main = """
from meta import main
main()
"""
    print(timeit.repeat(stmt=main
                        , repeat=1, number=1))

    print_file("meta.py")
