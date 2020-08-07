import timeit


def open_python_file(python_filename):

    # Initialize empty string variable
    python_code = ""

    try:
        # Open python file in read-mode
        f = open(python_filename, 'r')
    except FileNotFoundError as e:
        print(e)
        raise e
    finally:
        f.close()
        return


    # For each line of code in file that's not blank, append to python_code variable (and print it for debugging)
    for code in f:
        if code is not "\n":
            python_code += code
    return python_code


def time_python_code(python_filename):
    # Open python file and store it as a string
    code = open_python_file(python_filename)

    # Return the time it took for python file to execute!
    return timeit.repeat(stmt=code, repeat=1, number=1)[0]


if __name__ == '__main__':
    testvar = "test"
    exec('print(testvar)')

    meta_file = "meta.py"
    execly_file = "execly.py"
    timed_code = {meta_file: time_python_code(meta_file),
                  execly_file: time_python_code(execly_file)}
    """
    print("Meta.py execution time:",timed_code[meta_file],"\n",
          "Execly.py execution time:",timed_code[execly_file],"\n",
          "Execly.py is",str(int(timed_code[meta_file]/timed_code[execly_file])),"times faster than Meta.py!!"

          )
    """
    calculation = 5 * 300000000
    print("Calculating multiplication", str(calculation), "=", calculation, "took this long:",
          timeit.repeat(stmt=str(calculation), repeat=1, number=1)[0])
