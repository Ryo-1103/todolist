from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from rest_framework import viewsets

from .forms import TodoItemForm
from .models import TodoItem
from .serializers import TodoItemSerializer


@login_required
def todo_list(request):
    if request.method == "POST":
        form = TodoItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("todo_list")
    else:
        form = TodoItemForm()

    todo_items = TodoItem.objects.all().order_by("priority", "created_at")
    edit_forms = {item.pk: TodoItemForm(instance=item) for item in todo_items}
    context = {"todo_items": todo_items, "form": form, "edit_forms": edit_forms}
    return render(request, "list/todo_list.html", context)


def edit_todo_item(request, pk):
    item = get_object_or_404(TodoItem, pk=pk)
    if request.method == "POST":
        form = TodoItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("todo_list")
    else:
        form = TodoItemForm(instance=item)
    return render(request, "list/edit_todo_item.html", {"form": form, "item": item})


def complete_todo_item(request, pk):
    todo_item = get_object_or_404(TodoItem, pk=pk)
    todo_item.completed = True
    todo_item.save()
    return redirect("todo_list")


def incomplete_todo_item(request, pk):
    todo_item = get_object_or_404(TodoItem, pk=pk)
    todo_item.completed = False
    todo_item.save()
    return redirect("todo_list")


def delete_todo_item(request, pk):
    todo_item = get_object_or_404(TodoItem, pk=pk)
    todo_item.delete()
    return redirect("todo_list")


def get_edit_form(request, pk):
    item = get_object_or_404(TodoItem, pk=pk)
    form = TodoItemForm(instance=item)
    html = render_to_string("list/edit_form.html", {"form": form}, request=request)
    return JsonResponse({"html": html})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("todo_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


class TodoItemViewSet(viewsets.ModelViewSet):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
