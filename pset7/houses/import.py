from sys import argv, exit
import csv
import cs50

# check number of command line arguments. If incorrect print error and exit
if len(argv) != 2:
    print("incorrect number of command line arguments specified.")
    exit(1)

# open csv file
with open(argv[1], "r") as csvfile:
    students = csv.DictReader(csvfile)

    db = cs50.SQL("sqlite:///students.db")

    # extract items from keys
    for row in students:
        house = row['house']
        birth = row['birth']

        # put split names list into first, middle and last
        name = row['name'].split()
        first = name[0]
        last = name[-1]
        middle = None
        if len(name) == 3:
            middle = name[1]

        # copy elements into sql table
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES ( ?, ?, ?, ?, ?)", first, middle, last, house, birth)

exit(0)