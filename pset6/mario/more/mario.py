def pyramid():
    # check validity of input
    while True:
        try:
            n = int(input("Height: "))
        except ValueError:
            continue
        if n > 0 and n < 9:
            break

    # pyramid
    for j in range(1, n + 1):
        # print leading spaces on each line
        print(" " * (n - j), end='')
        # print first set of hashes and middle gap
        print("#" * j, end='  ')
        # print second set of hashes
        print("#" * j)


pyramid()