from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from reviews.models import (Comment, Review, Category, Genre,
                            Title, GenreTitle, User)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for row in DictReader(
            open('./static/data/users.csv', encoding='utf-8')
        ):
            user = User(
                id=row['id'], username=row['username'],
                email=row['email'], role=row['role'],
                bio=row['bio'], first_name=row['first_name'],
                last_name=row['last_name']
            )
            user.save()
        for row in DictReader(
            open('./static/data/category.csv', encoding='utf-8')
        ):
            category = Category(
                id=row['id'], name=row['name'], slug=row['slug']
            )
            category.save()
        for row in DictReader(
            open('./static/data/genre.csv', encoding='utf-8')
        ):
            genre = Genre(id=row['id'], name=row['name'], slug=row['slug'])
            genre.save()
        for row in DictReader(
            open('./static/data/titles.csv', encoding='utf-8')
        ):
            title = Title(
                id=row['id'], name=row['name'],
                year=row['year'], category_id=row['category']
            )
            title.save()
        for row in DictReader(
            open('./static/data/review.csv', encoding='utf-8')
        ):
            review = Review(
                id=row['id'], title_id=row['title_id'],
                text=row['text'], author_id=row['author'],
                score=row['score'],
                pub_date=datetime.strptime(row['pub_date'],
                                           '%Y-%m-%dT%H:%M:%S.%fZ')
            )
            review.save()
        for row in DictReader(
            open('./static/data/comments.csv', encoding='utf-8')
        ):
            comment = Comment(
                id=row['id'], review_id=row['review_id'],
                text=row['text'], author_id=row['author'],
                pub_date=datetime.strptime(row['pub_date'],
                                           '%Y-%m-%dT%H:%M:%S.%fZ')
            )
            comment.save()
        for row in DictReader(
            open('./static/data/genre_title.csv', encoding='utf-8')
        ):
            genretitle = GenreTitle(
                id=row['id'], genre_id=row['genre_id'],
                title_id=row['title_id'],

            )
            genretitle.save()
