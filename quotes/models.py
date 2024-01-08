import datetime
import json
from django.db import models
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
import random

# python manage.py makemigrations
# python manage.py migrate
# TODO fix code format

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author)
    genres = models.ManyToManyField(Genre)
    cover = models.ImageField(default='default.jpg', upload_to='media/', blank=True)

    def __str__(self):
        return self.title
    
class BookQuote(models.Model):
    content = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    upvotes = models.ManyToManyField(User, blank=True, related_name="upvotes")
    downvotes = models.ManyToManyField(User, blank=True, related_name="downvotes")

    def snippet(self):
        if len(self.content) > 50:
            return f"\"{str(self.content[:50])}...\" - {str(self.author)}"
        else:
            return f"\"{str(self.content[:50])}\" - {str(self.author)}"

    def __str__(self):
        return self.snippet()
    
    def total_votes(self): 
        return self.upvotes.count() - self.downvotes.count()

class Score(models.Model):
    # Scores is a json of entries {"score": score, "timestamp": timestmap}.
    scores = models.TextField(null=True, blank=True)
    # If you inherit the Score model multiple times, override this field with
    # an unique related_name keyword.
    past_quotes = models.ManyToManyField(BookQuote, blank=True)
    # Also override this with an unique related_name keyword.
    current_quote = models.ForeignKey(BookQuote, on_delete=models.SET_NULL, 
                                      null=True, blank=True)
    # Time when the quiz started. Used to tell when to finish quiz.
    start_time = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.current_quote:
            self.get_random_quote()
        if not self.scores:
            timestamp = str(datetime.datetime.now())
            self.scores = json.dumps([{"score": 0, "timestamp": timestamp}])
        super().save(*args, **kwargs)

    def get_random_quote(self):
        if self.current_quote:
            self.past_quotes.add(self.current_quote)
            self.save()
        self.current_quote = random.choice(list(BookQuote.objects.all()))

    def get_scores(self):
        return json.loads(self.scores)

    def update_score(self, new_score):
        timestamp = str(datetime.datetime.now())
        previous_scores = self.get_scores()
        previous_scores.append({"score": new_score, "timestamp": timestamp})
        self.scores = json.dumps(previous_scores)
        self.save()

    def check_title(self, title):
        """Compare the titles to update score. Then get a new quote."""
        previous_scores = self.get_scores()
        if self.current_quote.book.title == title:
            self.update_score(previous_scores[-1]["score"] + 10)
        else:
            self.update_score(previous_scores[-1]["score"] - 10)
        self.get_random_quote()
        self.save()

    def get_book_choices(self):
        """Give 4 possible books that the quote belongs to."""
        # Get a list of 3 random authors and the author from the above quote.
        # Make sure to exclude correct author from random choices.

        current_quote_genres = self.current_quote.book.genres.all()

        # Get a list of books with similar genres (excluding the current quote's book)
        similar_books = Book.objects.filter(genres__in=current_quote_genres).exclude(id=self.current_quote.book.id).distinct()

        try:
            selected_books = random.sample(list(similar_books), 3)
        except:
            possible_books = list(Book.objects.all())
            possible_books.remove(self.current_quote.book)
            selected_books = random.sample(possible_books, 3)

        # Create a copy of selected_books before appending the current quote's book
        selected_books_copy = selected_books.copy()
        
        selected_books_copy.append(self.current_quote.book)
        random.shuffle(selected_books_copy)

        return selected_books_copy

    def __str__(self):
        return str(self.start_time) + "\n" + str(self.scores)

class GuestScore(Score):
    user_session = models.ForeignKey(Session, on_delete=models.CASCADE)
    past_quotes = models.ManyToManyField(BookQuote, related_name='guest_scores', blank=True)
    current_quote = models.ForeignKey(BookQuote, related_name='current_guest_score', on_delete=models.SET_NULL, null=True, blank=True)

class UserScore(Score):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    past_quotes = models.ManyToManyField(BookQuote, related_name='user_scores', blank=True)
    current_quote = models.ForeignKey(BookQuote, related_name='current_user_score', on_delete=models.SET_NULL, null=True, blank=True)

class SavedScores(models.Model):
    # Create a String containing scores in format {score1},{score2},{score3}...
    # Same format for start_times and durations
    scores =  models.TextField(null=True, blank=True)
    start_times = models.TextField(null=True, blank=True)
    durations = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_scores(self):
        if self.scores:
            return self.scores.split(',')
        else:
            return []
        
    def get_start_times(self):
        if self.start_times:
            return self.start_times.split(",")
        else:
            return []
        
    def get_durations(self):
        if self.durations:
            return self.durations.split(",")
        else:
            return []

    def append_score(self, score, start_time, duration):
        try:
            self.scores += "," + str(score)
            self.start_times += "," + str(start_time)
            self.durations += "," + str(duration)
        except TypeError:
            self.scores = str(score)
            self.start_times = str(start_time)
            self.durations = str(duration)
        self.save()