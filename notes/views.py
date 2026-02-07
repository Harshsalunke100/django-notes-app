import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

API_BASE_URL = "http://127.0.0.1:8000/api/notes/"

@login_required
def note_list(request):
    response = requests.get(API_BASE_URL)
    notes = response.json()
    return render(request, 'notes/list.html', {'notes': notes})

@login_required
def note_create(request):
    if request.method == "POST":
        data = {
            "title": request.POST.get("title"),
            "content": request.POST.get("content"),
            "user": request.user.id
        }
        requests.post(API_BASE_URL, json=data)
        return redirect('note_list')

    return render(request, 'notes/form.html')

@login_required
def note_update(request, pk):
    if request.method == "POST":
        data = {
            "title": request.POST.get("title"),
            "content": request.POST.get("content"),
            "user": request.user.id
        }
        requests.put(f"{API_BASE_URL}{pk}/", json=data)
        return redirect('note_list')

    note = requests.get(f"{API_BASE_URL}{pk}/").json()
    return render(request, 'notes/form.html', {'note': note})

@login_required
def note_delete(request, pk):
    requests.delete(f"{API_BASE_URL}{pk}/")
    return redirect('note_list')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('note_list')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})
