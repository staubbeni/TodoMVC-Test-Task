import pytest
from playwright.sync_api import Page, expect


@pytest.fixture
def add_todo(page: Page):
    """Open the app and return a function that adds a todo by its text."""
    page.goto("https://demo.playwright.dev/todomvc/#/")
    new_todo = page.get_by_placeholder("What needs to be done?")

    def _add(text: str):
        new_todo.fill(text)
        new_todo.press("Enter")

    return _add


@pytest.mark.parametrize(
    "text",
    ["Buy groceries", "買い物をする", "Get a 6-pack for the party on 10.09."],
    ids=["english", "non_english", "numbers"],
)
def test_add_todo(page: Page, add_todo, text):
    add_todo(text)
    expect(page.get_by_test_id("todo-title")).to_have_text([text])


def test_can_be_completed(page: Page, add_todo):
    add_todo("Complete this task")
    todo_item = page.get_by_test_id("todo-item").filter(has_text="Complete this task")
    todo_item.get_by_role("checkbox").check()
    page.get_by_role("link", name="Completed").click()
    expect(todo_item).to_have_class("completed")
    expect(page.get_by_test_id("todo-item")).to_have_text(["Complete this task"])


def test_can_be_deleted(page: Page, add_todo):
    add_todo("Delete this task")
    # A second todo keeps the footer (and its filter links) visible after the delete
    add_todo("Keep this task")
    todo_item = page.get_by_test_id("todo-item").filter(has_text="Delete this task")
    todo_item.hover()  # Delete button is only visible on hover
    todo_item.get_by_role("button", name="Delete").click()
    for view in ["All", "Active", "Completed"]:
        page.get_by_role("link", name=view).click()
        expect(
            page.get_by_test_id("todo-title").filter(has_text="Delete this task")
        ).to_have_count(0)
    for view in ["All", "Active"]:
        page.get_by_role("link", name=view).click()
        expect(
            page.get_by_test_id("todo-title").filter(has_text="Keep this task")
        ).to_have_count(1)


def test_active_filter(page: Page, add_todo):
    add_todo("Active task")
    add_todo("Completed task")
    completed_item = page.get_by_test_id("todo-item").filter(has_text="Completed task")
    # Complete one of two tasks, so the Active filter has something to hide
    completed_item.get_by_role("checkbox").check()
    page.get_by_role("link", name="Active").click()
    expect(page.get_by_test_id("todo-item")).to_have_count(1)
    expect(page.get_by_test_id("todo-item")).to_have_text(["Active task"])


def test_completed_filter(page: Page, add_todo):
    add_todo("Completed task")
    # Keep an active task, so the Completed filter has something to hide
    add_todo("Active task")
    completed_item = page.get_by_test_id("todo-item").filter(has_text="Completed task")
    completed_item.get_by_role("checkbox").check()
    page.get_by_role("link", name="Completed").click()
    expect(page.get_by_test_id("todo-item")).to_have_count(1)
    expect(page.get_by_test_id("todo-item")).to_have_text(["Completed task"])
