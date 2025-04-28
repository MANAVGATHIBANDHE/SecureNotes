# notes/views.py

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login
from django.contrib.auth import logout

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models      import Q

from .forms import NoteForm
from .models import Note


# Create your views here.

def welcome_view(request):
    return render(request, 'welcome.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after successful signup
            return redirect('dashboard')  # 🚀 We will create 'dashboard' view later
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')  # 🚀 Redirect after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('welcome')

@login_required
def create_note_view(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user  # 👈 Link note to the logged-in user
            note.save()
            return redirect('dashboard')  # After adding note, go back to dashboard (we'll show notes there later)
    else:
        form = NoteForm()
    return render(request, 'create_note.html', {'form': form})

@login_required
def list_notes(request):
    q = request.GET.get('q', '').strip()
    # Fetch only notes belonging to the logged-in user, ordered newest first
    notes_qs = Note.objects.filter(user=request.user).order_by('-created_at')
    if q:
        notes_qs = notes_qs.filter(
            Q(title__icontains=q) | Q(content__icontains=q)
        )
    notes_qs = notes_qs.order_by('-created_at')

    paginator   = Paginator(notes_qs, 5)             # 5 notes per page
    page_number = request.GET.get('page')
    page_obj    = paginator.get_page(page_number)
    
    return render(request, 'list_notes.html', {
        'page_obj': page_obj,
        'q': q,
    })

@login_required
def detail_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'detail_note.html', {'note': note})

@login_required
def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('list_notes')
    else:
        form = NoteForm(instance=note)
    return render(request, 'edit_note.html', {'form': form})

@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('list_notes')
    return render(request, 'delete_note.html', {'note': note})