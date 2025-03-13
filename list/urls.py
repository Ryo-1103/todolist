from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TodoItemViewSet,
    complete_todo_item,
    delete_todo_item,
    edit_todo_item,
    get_edit_form,
    incomplete_todo_item,
    todo_list,
)

router = DefaultRouter()
router.register(r"api/todos", TodoItemViewSet)

urlpatterns = [
    path("", todo_list, name="todo_list"),
    path("edit/<int:pk>/", edit_todo_item, name="edit_todo_item"),
    path("complete/<int:pk>/", complete_todo_item, name="complete_todo_item"),
    path("incomplete/<int:pk>/", incomplete_todo_item, name="incomplete_todo_item"),
    path("delete/<int:pk>/", delete_todo_item, name="delete_todo_item"),
    path("", include(router.urls)),
    # 他のURLパターン
]
