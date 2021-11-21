from django.core.management.base import BaseCommand
import csv
import sqlite3
connect = sqlite3.connect('db.sqlite3')
new_data = connect.cursor()


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('static/data/comments.csv', encoding='utf-8') as data:
            reader = csv.DictReader(data)
            for row in reader:
                id = row['id']
                pub_date = row['pub_date']
                author_id = row['author']
                review_id = row['review_id']
                text = row['text']
                new_data.execute(
                    "INSERT INTO reviews_comments "
                    "(id, pub_date, author_id, review_id, text)"
                    "VALUES(?, ?, ?, ?, ?)",
                    (id, pub_date, author_id, review_id, text)
                )
                connect.commit()
        with open('static/data/category.csv', encoding='utf-8') as data:
            reader = csv.DictReader(data)
            for row in reader:
                id = row['id']
                name = row['name']
                slug = row['slug']
                new_data.execute(
                    "INSERT INTO reviews_category "
                    "(id, name, slug)"
                    "VALUES(?, ?, ?)",
                    (id, name, slug)
                )
                connect.commit()
        with open('static/data/genre_title.csv', encoding='utf-8') as data:
            reader = csv.DictReader(data)
            for row in reader:
                id = row['id']
                title_id = row['title_id']
                genre_id = row['genre_id']
                new_data.execute(
                    "INSERT INTO reviews_title_genres "
                    "(id,title_id,genre_id)"
                    "VALUES(?, ?, ?)",
                    (id, title_id, genre_id)
                )
                connect.commit()
        with open('static/data/genre.csv', encoding='utf-8') as data:
            reader = csv.DictReader(data)
            for row in reader:
                id = row['id']
                name = row['name']
                slug = row['slug']
                new_data.execute(
                    "INSERT INTO reviews_genres "
                    "(id, name, slug)"
                    "VALUES(?, ?, ?)",
                    (id, name, slug)
                )
                connect.commit()
        with open('static/data/titles.csv', encoding='utf-8') as data:
            reader = csv.DictReader(data)
            for row in reader:
                id = row['id']
                name = row['name']
                year = row['year']
                category_id = row['category']
                new_data.execute(
                    "INSERT INTO reviews_title "
                    "(id,name,year,category_id)"
                    "VALUES(?, ?, ?, ?)",
                    (id, name, year, category_id)
                )
                connect.commit()
        with open('static/data/review.csv', encoding='utf-8') as data:
            reader = csv.DictReader(data)
            for row in reader:
                id = row['id']
                title_id = row['title_id']
                text = row['text']
                author_id = row['author']
                pub_date = row['pub_date']
                score = row['score']
                new_data.execute(
                    "INSERT INTO reviews_review "
                    "(id, title_id, text, author_id, score, pub_date)"
                    "VALUES(?, ?, ?, ?, ?, ?)",
                    (id, title_id, text, author_id, score, pub_date)
                )
                connect.commit()
                connect.close()
