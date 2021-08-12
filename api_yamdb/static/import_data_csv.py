import csv
from os import error

from reviews.models import User

CSV_USERS = 'static/data/users.csv'

contSuccess = 0

with open(CSV_USERS, newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    print('Loading...')
    for row in csvreader:
        try:
            User.objects.get_or_create(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
                first_name=row[5],
                last_name=row[6])
            contSuccess += 1
        except error:
            print("there was a problem with line", row)
    print(f'{str(contSuccess)} inserted successfully!')
