from django.contrib import admin
from .models import Genre, Author, Book, BookQuote, GuestScore, SavedScores, UserScore

admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookQuote)
admin.site.register(GuestScore)
admin.site.register(UserScore)
admin.site.register(SavedScores)