import ast
from datetime import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from .models import BookQuote, GuestScore, SavedScores, UserScore
from . import forms

def quotes_view(request):
    # User will be an empty String if they are not logged in.
    user = ""
    if request.user.is_authenticated:
        user = request.user

    # Check if user has selected a time duration.
    if request.method == 'POST' and request.POST.get('action') == 'duration':
        form = forms.QuizDurationForm(request.POST)
        if form.is_valid():
            duration = form.cleaned_data['duration']
            # Create user/guest score.
            if user:
                UserScore.objects.create(user=user, 
                                         start_time=timezone.now(),
                                         duration=duration)
            else:
                # Create/Find user session for maintaining score.
                if not request.session.session_key:
                    request.session.save()
                user_session = Session.objects.get(session_key=request.session.session_key)
                GuestScore.objects.create(user_session=user_session,
                                          start_time=timezone.now(),
                                          duration=duration)
        else:
            return render(request, "quotes/start.html", {'form': form})

    # Try and get current score. If quiz has not started, render start.html 
    # which asks for type of quiz.
    score = ""
    if user:
        # Get/Create user score.
        try:
            score = UserScore.objects.get(user=user)
        except UserScore.DoesNotExist:
            form = forms.QuizDurationForm()
            return render(request, "quotes/start.html", {"form": form})
    else:
        # Create/Find user session for maintaining score.
        if not request.session.session_key:
            request.session.save()
        user_session = Session.objects.get(session_key=request.session.session_key)
        # Get/Create guest score.
        try:
            score = GuestScore.objects.get(user_session=user_session)
        except GuestScore.DoesNotExist:
            form = forms.QuizDurationForm()
            return render(request, "quotes/start.html", {"form": form})

    # Check user's answer and update score if they answered.
    if request.method == 'POST' and request.POST.get('action') == 'answer':
        user_answer = request.POST.get('user_answer')
        score.check_title(user_answer)

    current_time = timezone.now()
    elapsed_time = (current_time - score.start_time).total_seconds()
    remaining_time = (int) (score.duration - elapsed_time)

    # Finish quiz if time is up.
    if remaining_time <= 0:
        if user:
            savedScores = ""
            try:
                savedScores = SavedScores.objects.get(user=user)
            except SavedScores.DoesNotExist:
                savedScores = SavedScores.objects.create(user=user)
            recent_score = score.get_scores()[-1]
            savedScores.append_score(recent_score["score"], score.start_time,
                                     score.duration)
        final_score = score.get_scores()[-1]["score"]
        past_quotes = score.past_quotes.all()
        past_quotes_ids = [past_quote.id for past_quote in past_quotes]
        score.delete()

        return render(request, 
                      "quotes/result.html", 
                      {"score": final_score,
                       "past_quotes": past_quotes,
                       "past_quotes_ids": past_quotes_ids})

    return render(request, 'quotes/quote_quiz.html', 
                  {"bookquote": score.current_quote,
                   "books": score.get_book_choices(),
                   "scores": score.get_scores(),
                   "user": user,
                   "time": score.start_time,
                   "remaining_time": remaining_time,
                   "max_time": score.duration})

@login_required
def scores_view(request):
    savedScores = ""
    try:
        savedScores = SavedScores.objects.get(user=request.user)
    except SavedScores.DoesNotExist:
        savedScores = SavedScores.objects.create(user=request.user)

    # Get the scores and start times
    scores = savedScores.get_scores()

    # Convert scores to integers
    scores = [int(score) for score in scores]

    # Format start times to show up to seconds without timezone
    start_times = [datetime.fromisoformat(time).replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S') 
                   for time in savedScores.get_start_times()]

    durations = savedScores.get_durations()

    score_tuples = list(zip(scores, start_times, durations))

    # Sort by the first element (scores) in each tuple
    sorted_score_tuples = sorted(score_tuples, key=lambda x: x[0], reverse=True)

    # Get top 50 scores
    sorted_score_tuples = sorted_score_tuples[:50]

    return render(request, "quotes/scores.html", {"sorted_score_tuples": sorted_score_tuples})

@login_required
def create_quote_view(request):
    if request.method == 'POST':
        form = forms.BookQuoteForm(request.POST)
        if form.is_valid:
            quote = form.save(commit=False)
            quote.save()
            return redirect("quotes")
    else: 
        form = forms.BookQuoteForm()
    return render(request, "quotes/create_quote.html", {"form": form})

@login_required
def create_book_view(request):
    if request.method == 'POST':
        form = forms.BookForm(request.POST, request.FILES)
        if form.is_valid:
            book = form.save(commit=False)
            book.save()
            return redirect("create_quote")
    else:
        form = forms.BookForm()
    return render(request, "quotes/create_book.html", {"form": form})

@login_required
def create_author_view(request):
    if request.method == 'POST':
        form = forms.AuthorForm(request.POST)
        if form.is_valid:
            author = form.save(commit=False)
            author.save()
            return redirect("create_quote")
    else:
        form = forms.AuthorForm()
    return render(request, "quotes/create_author.html", {"form": form})

@login_required
def upvote_view(request):
    book_quote = get_object_or_404(BookQuote, id=request.POST.get('quote_id'))

    if request.POST.get('vote_type') == "upvote":
        if not book_quote.upvotes.filter(id=request.user.id).exists():
            book_quote.upvotes.add(request.user)
            if book_quote.downvotes.filter(id=request.user.id).exists():
                book_quote.downvotes.remove(request.user)
        else:
            book_quote.upvotes.remove(request.user)
    else:
        if not book_quote.downvotes.filter(id=request.user.id).exists():
            book_quote.downvotes.add(request.user)
            if book_quote.upvotes.filter(id=request.user.id).exists():
                book_quote.upvotes.remove(request.user)
        else:
            book_quote.downvotes.remove(request.user)

    score = request.POST.get('score')
    past_quotes_ids = ast.literal_eval(request.POST.get('past_quotes_ids'))
    past_quotes = [get_object_or_404(BookQuote, id=id) for id in past_quotes_ids]

    return render(request, 
                  "quotes/result.html", 
                  {"score": score,
                   "past_quotes": past_quotes,
                   "past_quotes_ids": past_quotes_ids})