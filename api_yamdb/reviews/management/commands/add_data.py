import csv

from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('static/data/category.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                category, created = Category.objects.update_or_create(
                    id=row['id'], name=row['name'],
                    slug=row['slug']
                )
        with open('static/data/genre.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                genre, created = Genre.objects.update_or_create(
                    id=int(row['id']), name=row['name'],
                    slug=row['slug']
                )
        with open('static/data/titles.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title, created = Title.objects.update_or_create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category'],
                )
        with open('static/data/genre_title.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                exists, created = GenreTitle.objects.update_or_create(
                    title_id=row['title_id'],
                    genre_id=row['genre_id']
                )
        with open('static/data/users.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                user, created = User.objects.update_or_create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                )
        with open('static/data/review.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                review, created = Review.objects.update_or_create(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author_id=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date']
                )
        with open('static/data/comments.csv', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                comment, created = Comment.objects.update_or_create(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author_id=row['author'],
                    pub_date=row['pub_date']
                )
