from django import forms
from django_select2 import forms as s2forms

from . import models

class QuizDurationForm(forms.Form):
    DURATION_CHOICES = (
        (30, 'short'),
        (60, 'medium'),
        (90, 'long'),
    )

    duration = forms.ChoiceField(
        choices=DURATION_CHOICES,
        widget=forms.HiddenInput(),  # Hide the default radio buttons
    )

class AuthorWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]

class BookWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "title__icontains",
    ]

class GenresWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__icontains",
    ]

class AuthorsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__icontains",
    ]

class BookQuoteForm(forms.ModelForm):
    class Meta:
        model = models.BookQuote
        fields = ['content', 'book', 'author']
        widgets = {
            'author': AuthorWidget,
            'book': BookWidget,
        }
        
class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = {"title", "authors", "genres", "cover"}
        widgets = {
            "authors": AuthorsWidget,
            "genres": GenresWidget,
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = models.Author
        fields = {"name"}