from sys import exit

# get number
while True:
    try:
        n = int(input("Number: "))
    except ValueError:
        continue
    if n > 0:
        break

# copy number to manipulate
num = n
remainders = 0
doubles = 0


card_len = len(str(num))

if card_len < 13 or card_len == 14 or card_len > 16:
    print("INVALID")
    exit(0)

# calculate checksum components
while num > 0:
    # sum remainder numbers
    remainders += num % 10

    # removing last digit from num
    num = (num - (num % 10)) / 10

    holder = (num % 10) * 2

    # doubling number and summing if greater than 10
    if holder >= 10:
        doubles += 1 + (holder % 10)
    else:
        doubles += holder

    # removing digit from number
    num = (num - (num % 10)) / 10

checksum = doubles + remainders

# checking checksum value
if checksum % 10 != 0:
    print("INVALID")
    exit(0)
else:
    # getting first two digits of card.
    digits = int(str(n)[:2])

    if card_len == 15:
        if digits == 34 or digits == 37:
            print("AMEX")
        else:
            print("INVALID")
    elif card_len == 16:
        if digits > 39 and digits < 50:
            print("VISA")
        elif digits > 50 and digits < 56:
            print("MASTERCARD")
        else:
            print("INVALID")
    elif card_len == 13:
        if digits > 39 and digits < 50:
            print("VISA")
        else:
            print("INVALID")
    else:
        print("INVALID")