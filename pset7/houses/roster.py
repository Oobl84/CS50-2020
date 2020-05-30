from sys import argv, exit
from cs50 import SQL

if len(argv) != 2:
    print("incorrect number of arguments specified")
    exit(1)

# validating houses
elif argv[1].lower() not in ["gryffindor", "hufflepuff", "ravenclaw", "slytherin"]:
    print("please specify a valid housename")
    exit(2)

# changing input to title case for searching sql db
house = argv[1].title()

db = SQL("sqlite:///students.db")

# executing SQL query
roster = db.execute('SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first', house)

for i in roster:
    if i['middle'] is None:
        print(i['first'] + " " + i['last'] + ", born " + str(i['birth']))
    else:
        print(i['first'] + " " + i['middle'] + " " + i['last'] + ", born " + str(i['birth']))

exit(0)