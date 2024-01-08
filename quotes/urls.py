from django.contrib import admin
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.quotes_view, name="quotes"), 
    re_path(r'^scores$', views.scores_view, name="scores"),
    re_path(r'^create-quote', views.create_quote_view, name="create_quote"),
    re_path(r'^create-book', views.create_book_view, name="create_book"),
    re_path(r'^create-author', views.create_author_view, name="create_author"),
    re_path(r'^upvote', views.upvote_view, name="upvote_quote")
]