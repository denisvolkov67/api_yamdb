import csv

from reviews.models import User, Categories, Genres, Title, Review, Comment


CSV_USERS = 'static/data/users.csv'
CSV_CATEGORY = 'static/data/category.csv'
CSV_GENRE = 'static/data/genre.csv'
CSV_TITLE = 'static/data/titles.csv'
CSV_REVIEW = 'static/data/review.csv'
CSV_COMMENTS = 'static/data/comments.csv'


print('start import')

with open(CSV_USERS, newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
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
        except ValueError:
            print("there was a problem with line", row)

with open(CSV_CATEGORY, newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        try:
            Categories.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2])
        except ValueError:
            print("there was a problem with line", row)

with open(CSV_GENRE, newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        try:
            Genres.objects.get_or_create(
                id=row[0],
                name=row[1],
                slug=row[2])
        except ValueError:
            print("there was a problem with line", row)

with open(CSV_TITLE, newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        try:
            Title.objects.get_or_create(
                id=row[0],
                name=row[1],
                year=row[2],
                category_id=row[3])
        except ValueError:
            print("there was a problem with line", row)

with open(CSV_REVIEW, newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        try:
            Review.objects.get_or_create(
                id=row[0],
                title_id=row[1],
                text=row[2],
                author_id=row[3],
                score=row[4],
                pub_date=row[5])
        except ValueError:
            print("there was a problem with line", row)

with open(CSV_COMMENTS, newline='', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        try:
            Comment.objects.get_or_create(
                id=row[0],
                review_id=row[1],
                text=row[2],
                author_id=row[3],
                pub_date=row[4])
        except ValueError:
            print("there was a problem with line", row)

print('Inserted successfully!')
