from sys import argv, exit
import csv
import re


if len(argv) != 3:
    print("Usage: dna.py data.csv sequence.txt")
    exit(1)
elif re.match(".*\.csv$", argv[1]) is None or re.match(".*\.txt$", argv[2]) is None:
    print("Usage: dna.py data.csv sequence.txt")
    exit(2)
else:
    # opening csvfile
    with open(argv[1], "r") as csvfile:
        database = csv.DictReader(csvfile)

        # creating dictionary to hold value counts
        # getting columns from first row
        seq_count = dict(next(database))

        # remove name key
        del seq_count['name']

        # count number of keys
        key_count = len(seq_count)

        # set values = 0
        for key in seq_count:
            seq_count[key] = 0

        # checking sequence for repeating patterns
        with open(argv[2], "r") as txtfile:
            sequence = csv.reader(txtfile)

            # getting sequence length
            for row in sequence:
                line = row[0]
                length = len(line)

            # getting pattern to check
            for key in seq_count:
                pat_len = len(key)
                flag = 0
                repeat_count = 0
                repeats = [0]

                # checking loop for pattern
                i = 0
                while (length - i) >= pat_len:
                    # getting slice to compare
                    section = line[i: pat_len + i]
                    # actions on match
                    if section == key:
                        flag = 1
                        repeat_count += 1
                        i += pat_len
                    else:
                        # if matches found append to list
                        if flag == 1:
                            repeats.append(repeat_count)
                            repeat_count = 0
                            flag = 0
                            i += 1
                        # otherwise just check from the next sequence
                        else:
                            i += 1

                # set repeats value in dictionary
                seq_count[key] = max(repeats)

            # rewind file and check values in database
            csvfile.seek(0)
            next(csvfile)
            for row in database:
                checker = dict(row)
                check_count = 0
                for key in seq_count:
                    if seq_count[key] == int(checker[key]):
                        check_count += 1
                if check_count == key_count:
                    print(row['name'])
                    exit(0)

    print("No match")
    exit(0)